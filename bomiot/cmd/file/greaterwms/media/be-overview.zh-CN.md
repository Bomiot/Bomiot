# 后端架构总览

bomiot / GreaterWMS 后端基于 Django + Django REST Framework 构建，采用「框架 + 工作空间」的双层结构：`bomiot` 是通过 pip 安装的通用框架包，`greaterwms` 是位于工作目录的具体业务工程。本文从源码出发，描述整体目录结构、模块职责与关键设计。

## 1. 工程与框架的边界

- **bomiot 框架**：以 pip 包形式安装，源码位于 `site-packages/bomiot/`，提供 Django 配置、核心模型、信号调度、动态路由发现等通用能力。运行 `bomiot init` 时会从 `bomiot/cmd/file/setup.ini` 拷贝模板到工作目录作为工程根的 `setup.ini`。
- **greaterwms 工作空间**：位于 `e:\Github_desktop\bomiot_example\greaterwms\`，是实际的业务工程。`bomiotconf.ini` 中 `[mode] name = project` 标识其身份为「主工程」（区别于 `mode=plugins` 的插件目录或 pip 包插件）。

```ini
# greaterwms/bomiotconf.ini
[mode]
name = project
```

`setup.ini` 的 `[project] name = greaterwms` 字段被 `bomiot/server/server/settings.py` 读取为 `PROJECT_NAME`，决定项目子目录名、模板路径、媒体路径、语言包目录等。

## 2. bomiot 框架目录结构

框架主体位于 `bomiot/server/` 下，按职责划分：

```text
bomiot/
├── __init__.py              # 暴露 version() 入口
├── cmd/                     # 命令行实现（init / migrate / deploy 等）
│   └── file/setup.ini       # setup.ini 模板（init 时拷贝至工程根）
└── server/
    ├── manage.py            # Django 管理入口
    ├── bomiotconf.ini       # 框架自身的 mode 声明
    ├── server/              # Django 项目主模块
    │   ├── settings.py      # 动态 settings（动态发现 app、读 setup.ini）
    │   ├── urls.py           # 根 URL 路由（动态包含各 app 的 urls）
    │   ├── views.py          # 登录、首页、md 文件、favicon 等系统级视图
    │   ├── wsgi.py           # WSGI 入口
    │   └── pkgcheck.py       # 包/目录扫描、忽略名单
    ├── core/                # 核心运行时
    │   ├── models.py          # CoreModel / DataCoreModel 抽象基类 + 全部业务模型
    │   ├── handler.py         # 示例 Example ViewSet（业务模板）
    │   ├── views.py           # User / Team / Department / Permission 等系统 ViewSet
    │   ├── middlewares.py     # JwtAuthorizationMiddleware
    │   ├── auth.py            # CoreAuthentication（DRF 认证类）
    │   ├── jwt_auth.py        # create_token / parse_payload
    │   ├── permission.py      # CorePermission / NormalPermission
    │   ├── page.py            # DataCorePageNumberPagination 等分页器
    │   ├── throttle.py        # CoreThrottle（基于 ThrottleModel 的 IP 限流）
    │   ├── scheduler.py       # SchedulerManager（基于 APScheduler 的定时任务管理）
    │   ├── observer.py        # ObserverManager（watchdog 监听 media 目录）
    │   ├── server_monitor.py  # ServerManager（CPU/内存/磁盘/网络/PID 监控）
    │   ├── signal.py          # bomiot_signals / bomiot_data_signals 两条 Signal
    │   ├── utils.py            # receiver_callback / AST 反射 / 文件镜像等
    │   ├── filter.py          # 各模型的 django_filters FilterSet
    │   ├── serializers.py     # 各模型的 DRF Serializer
    │   ├── message.py         # i18n 消息封装（msg / detail / login / others）
    │   ├── apps.py            # CoreConfig.ready() 启动 monitor/scheduler/observer
    │   └── urls.py            # core 子路由（user/team/department + 全部业务路由）
    ├── function/             # 业务 ViewSet（与 core/models 一一对应）
    │   ├── goods.py  bin.py  stock.py  stock_bin.py
    │   ├── capital.py  supplier.py  customer.py
    │   ├── asn.py  asn_detail.py  dn.py  dn_detail.py
    │   ├── purchase.py  bar.py  fee.py  driver.py
    ├── language/             # 框架自带 i18n toml（en-US / zh-CN）
    ├── media/                # 框架自带文档与图片
    └── static/               # 框架自带静态资源
```

## 3. greaterwms 工程目录结构

工程根 `e:\Github_desktop\bomiot_example\greaterwms\`：

```text
greaterwms/
├── setup.ini             # 工程配置（init 时由模板生成，[project] name=greaterwms）
├── bomiotconf.ini        # mode=project，声明主工程身份
├── __init__.py            # 暴露 version()，从 gwms.__version__ 取版本
├── api.py                 # API 路由 → 函数名映射表（前端权限/菜单使用）
├── receiver.py            # 信号回调入口：业务处理类派发到 process 函数
├── task.py                # 定时任务函数（供 scheduler 通过 JobList 调用）
├── server.py              # 服务器类占位（默认全部注释）
├── files.py               # 文件相关辅助
├── auth/                  # 认证相关 Django app（apps.py 注册为 greaterwms.auth）
├── language/              # 工程自带 i18n toml（en-US / zh-CN）
├── process/               # 业务逻辑函数库
│   ├── goods.py  bin.py  supplier.py  customer.py
│   └── asn/  dn/          # 嵌套模块（status_1 / update / delete / shelving）
├── wms_process/           # 示例 Django app，apps.py 中注册 example_job 定时任务
├── templates/             # 前端 Quasar 工程（含 docs/ 目录）
├── fastapi_app/ flask_app/ x/ xxxxxxxxx/   # 其他实验/示例子工程
└── media/                 # 工程级媒体目录
```

## 4. 关键设计

### 4.1 基于信号的业务解耦

`bomiot/server/function/` 中的 ViewSet 不直接写业务逻辑，而是通过 `bomiot_data_signals.send_robust()` 发送信号：

```python
responses = bomiot_data_signals.send_robust(sender=self.__class__,
                                            request=self.request,
                                            mode='create',
                                            data=data)
```

信号由 `bomiot/server/core/utils.py` 的 `receiver_callback()` 接收，该函数通过 AST 解析项目根的 `receiver.py`，反射定位类与方法，再动态 `importlib` 加载执行。`receiver.py` 中的 `GoodsClass.goods_create` 等方法进一步委托给 `process/` 目录下的纯函数（如 `create_googs_process`）。ViewSet 拿到返回的 `msg` / `detail` / `login` 字典后再决定是否落库。

### 4.2 动态 App 发现

`bomiot/server/server/settings.py` 中 `load_dynamic_apps()` 在启动时扫描三类来源并加入 `INSTALLED_APPS`：

- `load_apps_from_packages()`：扫描已安装 pip 包，若包目录存在 `bomiotconf.ini` 且 `[mode] name = plugins`，且含 `apps.py`，则注册包名为 app。
- `load_apps_from_working_space()`：扫描工作目录下的子目录，同样按 `bomiotconf.ini` 的 `mode=plugins` 与 `apps.py` 注册。
- `load_apps_from_project()`：扫描 `WORKING_SPACE/PROJECT_NAME/` 下的子目录，凡含 `apps.py` 的均注册为 `PROJECT_NAME.app`（例如 `greaterwms.auth`、`greaterwms.wms_process`）。

### 4.3 JSON 字段模式

所有业务模型（Goods / Bin / Stock / Supplier / Customer / ASN / ASNDetail / DN / DNDetail / Purchase / Bar / Fee / Driver / Capital / StockBin / Example）均继承 `DataCoreModel` 且只声明一个：

```python
data = models.JSONField()
```

业务字段全部塞进 `data` 字典，新增字段无需迁移；查询通过 Django 的 `data__field` 跨界点语法实现，`filter.py` 中通过 `JSONFIELD_FILTER_OVERRIDE` 让 `django_filters` 支持对 JSON 子键的 `exact / contains / gte / lt / range` 等查询。

### 4.4 多项目隔离

`DataCoreModel` 抽象基类带 `project = models.CharField(max_length=255, default='bomiot')`。ViewSet 的 `get_queryset` 通过 `request.META.get('HTTP_PROJECT', settings.PROJECT_NAME)` 取得当前请求归属的工程名，并作为过滤条件，从而让同一张表能承载多个工程的数据。

### 4.5 软删除

`CoreModel` 与 `DataCoreModel` 都提供 `is_delete = models.BooleanField(default=False)`。所有 `get_queryset` 都会强制附加 `is_delete=False` 过滤；`GoodsDelete` 等 ViewSet 的 `delete()` 方法只做 `db_data.update(is_delete=True, updated_time=timezone.now())`，从不真正 `DELETE`。

### 4.6 部门隔离

业务数据查询额外注入 `data__department__gte: self.request.auth.department`，`department == 0` 视为管理员可见全部，其他用户只能看到自己部门及以上的数据。

### 4.7 后台服务

`bomiot/server/core/apps.py` 的 `CoreConfig.ready()` 在 worker 进程（`WORKERS` 环境变量 > 0）启动时通过文件锁防止重复启动，依次拉起：

- `start_monitoring()`：`ServerManager` 周期采集 CPU/内存/磁盘/网络/PID 写入对应模型，并通过 `bomiot_signals` 广播；
- `sm.start()`：`SchedulerManager` 每 60s 同步 `JobList` 表中的活跃任务到 APScheduler；
- `ob.start()`：`ObserverManager` 用 watchdog 监听 `MEDIA_ROOT`，把文件增删改同步到 `Files` 模型。

这三者共同构成系统监控、定时调度与媒体文件索引的后台能力，业务层通过 `bomiot_signals` 订阅事件即可扩展。
