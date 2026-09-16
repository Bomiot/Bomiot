#### Web端操作教程

[视频教程](https://www.bilibili.com/video/BV15r4y1i7Ph/)

#### 1.首页

- 解压后运行目录下的GreaterWMS-start.exe，等待初始化数据库以后,预计耗时10秒以内，会打开登录页面

![image-01](/media/img/shouye.jpg){ loading=lazy style="max-width: 100%" }

- 左下方为GreaterWMS的各个子模块，上方按钮分别为本地GreaterWMS的访问地址/GreaterWMS官方网站的地址/GWMS的苹果APP的下载地址/GWMS的Android APP下载地址/GreaterWMS的github源代码仓库url/语言选择/登录
- Android APP下载链接:为GWMS.apks的下载链接
- 语言:描述GreaterWMS支持的语言，目前支持简/繁体中文、法语、葡萄牙语、西班牙语、俄语、阿拉伯语，意大利语和日语。
- 登录：进入管理员/普通用户的登录页面

#### 2. 用户登录

- 点击首页上的登录按钮

![image-02](/media/img/userlogin.jpeg){ loading=lazy style="max-width: 100%" }

- 如果上次登录为用户登录，那这次点击登录就跳到用户登录页面来
- 用户名和验证码:由管理员提供，输入一致则登录成功，否则失败
- 如果验证码输入错误次数超过三次则该账户自动锁定，由管理员解锁方可登录

#### 4. 管理员登录

- 点击首页上的登录按钮

![image-03](/media/img/managerlogin.jpeg){ loading=lazy style="max-width: 100%" }
-
- 如果上次登录为管理员登录，那这次点击登录就跳到管理员登录页面来
- 管理员和密码：输入默认的管理员和密码admin/admin

#### 5. 首页-管理员登录

![image-04](/media/img/ManagerLogin-1.jpeg){ loading=lazy style="max-width: 100%" }

- 右下方不变还是各个子模块，上方按钮分别为本地GreaterWMS的访问地址/GreaterWMS官方网站的地址/GWMS的苹果APP的下载地址/GWMS的Android APP下载地址/GreaterWMS的github源代码仓库url/语言选择/登录
- 个人中心：由更改用户、查看OPENID组成

!!! info "用户"
    更改用户：改变当前已登录的用户
    查看OPENID：查看当前普通用户登录使用的信息

#### 6. 报表中心

- 具备报表中心权限可见

![image-05](/media/img/chuku.png){ loading=lazy style="max-width: 100%" }

- 点击报表中心-默认打开出库报表，即发货管理的数据，默认统计15天以内所创建的发货单的总销量
- 点击报表中心-点击收货报表，即收货管理的数据，默认统计15天以内所创建的到货通知书的总收货量
- 点击报表中心-点击收发货报表，即收货和发货的全部数据，统计系统所有的收货和发货的数量

#### 7. 收货管理

- 具备操作收货管理的权限可见

![image-06](/media/img/daohuo.jpg){ loading=lazy style="max-width: 100%" }

##### 7.1 点击收货管理

- 打开到货通知书列表-新增到货通知书

!!! info "ASN"

    新增到货通知书：

    1. 从列表中选择一个供应商名称

    2. 输入选择一个商品编码

    3. 输入数量

![image-07](/media/img/addshouhuo.jpeg){ loading=lazy style="max-width: 100%" }

!!! info "选取"

    从供应商列表中获取

    先输入前面几项数据，等搜索结果出来了再从结果里选择一个,比如输入一个00或者a，会弹出完整的商品编码，选择一个

![image-08](/media/img/mohuchaxun.png){ loading=lazy style="max-width: 100%" }

!!! info "输入"

    最后输入商品的数量，如果还想添加商品就继续在下一行的商品编码中输入，否则点击确定按钮

    刚添加的到货通知书，其初始状态为待到货

##### 7.2 点击收货管理

- 打开到货通知书列表-改变到货通知书状态

![image-09](/media/img/daohuozhuangtai.jpg){ loading=lazy style="max-width: 100%" }

- 其操作一栏的按钮分别为查看到货单、确认到货、确认卸货、确认分拣，编辑和删除
- 查看到货单：查看到货单详情，里面那个二维码供扫描枪去扫描
- 确认到货：限待到货状态的到货通知书点击此项，确认后状态更改为待卸货，删除待到货的数据，同时更新数据到待卸货。
- 确认卸货：限待卸货状态的到货通知书点击此项，确认后状态更改为待分拣，删除待卸货的数据，同时更新数据到待分拣。
- 确认分拣:  限待分拣状态的到货通知书点击此项，确认后输入实际到货数量，状态更改为已分拣，删除待分拣的数据，同时更新数据到已分拣。
- 编辑到货通知书：限待到货状态的到货通知书点击此项，与7.1类似，否则返回报错信息
- 删除到货通知书，限待到货状态的到货通知书点击此项，否则返回报错信息

##### 7.3 点击收货管理

- 点击已分拣-商品上架

![image-10](/media/img/shangjia.jpeg){ loading=lazy style="max-width: 100%" }

- 点击操作一栏下的上架按钮


![image-12](/media/img/shangjia1.jpeg){ loading=lazy style="max-width: 100%" }

- 输入库位名称：输入前面几项，从查询到的列表中选择一个
- 输入数量：输入数字，完成后正确的话不会提示，已分拣列表中删除刚才的数据，到货单状态更改为收货完成

#### 8. 发货管理

- 具备操作发货管理的权限可见

![image-13](https://po.56yhz.com/media/windows/fahuo.jpeg)

![image-12](/media/img/shangjia1.jpeg){ loading=lazy style="max-width: 100%" }

##### 8.1 点击发货管理

- 打开发货单列表-新增发货单

![image-13](/media/img/addfahuo.jpeg){ loading=lazy style="max-width: 100%" }

!!! info "新增"

    新增发货单：

    1. 从列表中选择一个客户名称

    2. 输入选择一个商品编码

    3. 输入数量

- 从客户列表中获取
- 先输入前面几项数据，等搜索结果出来了再从结果里选择一个,比如输入一个00或者a，会弹出完整的商品编码，选择一个

![image-14](/media/img/mohuchaxun.png){ loading=lazy style="max-width: 100%" }

!!! info "输入"

    最后输入商品的数量，如果还想添加商品就继续在下一行的商品编码中输入，否则点击确定按钮

    刚添加的发货单，其初始状态为预发货单

##### 8.2 点击发货管理

- 打开发货单列表-改变发货单状态


![image-16](/media/img/fahuozhuangtai.jpeg){ loading=lazy style="max-width: 100%" }

- 其操作一栏的按钮分别为查发货单、确认订单、生成拣货单、打印拣货单，确认拣货、装车发货、签收回单、编辑和删除按钮
- 查看发货单：查看发货单详情，里面那个二维码供扫描枪去扫描
- 确认订单：限预发货单状态的发货单点击此项，确认后状态更改为新发货单，删除预发货单的数据，同时更新数据到新发货单。
- 生成拣货单：限新发货单状态的发货单点击此项，库存数量足够则更改为待拣货，删除新发货单的数据，同时更新数据到待拣货；库存数量不足则进入欠货订单。
- 打印拣货单:  限待分拣状态的发货单点击此项，可以查看拣货单详情，里面那个二维码供扫描枪去扫描。
- 确认拣货完成：限待分拣状态的发货单点击此项，输入要拣货的数量，不要超过默认值，否则会报错，确认后状态更改为已拣货，删除待拣货的数据，更新到已拣货。
- 装车发货：限已拣货状态的发货单点击此项，否则返回报错信息，请输入司机名称中的几个字符，在弹出来的选择框中选择一个点击确定，状态更改为已发货，删除已拣货的数据，更新到已发货。

![image-17](/media/img/siji.png){ loading=lazy style="max-width: 100%" }

- 签收回单：限已发货状态的发货单点击此项，否则返回报错信息，请输入实际到货数量和到货破损数，点击确定按钮，状态更改为已签收，删除已发货的数据，更新到签收回单。

![image-18](/media/img/qianshou.jpeg){ loading=lazy style="max-width: 100%" }

#### 9. 库存管理

- 具备库存管理的权限可见

![image-16](/media/img/kucun.jpg){ loading=lazy style="max-width: 100%" }

- 分为库存列表、库位列表、空库位、有货库位、动态盘点和盘点记录
- 库存列表：记录了所有的商品变化信息
- 库位列表：记录了所有的库位变化信息
- 空库位：记录了无货的库位信息
- 有货库位：记录了存储了商品信息的库位信息
- 动态盘点：记录了15天以内发生变化的商品数据，盘点之后数据将进入盘点记录，动态盘点不会再有数据。
- 盘点记录：记录系统所有的盘点记录，选择日期所有相应的盘点记录

#### 10. 财务中心

- 具备操作财务中心的权限可见

![image-17](/media/img/caiwu.jpeg){ loading=lazy style="max-width: 100%" }

- 分为固定资产和运费管理两个子模块
- 固定资产：记录了固定资产信息,可新增，编辑和删除
- 运费管理：记录了运费信息，可新增，编辑和删除

#### 11. 商品管理

- 具备操作商品管理的权限可见

![image-18](/media/img/shangpin.jpg){ loading=lazy style="max-width: 100%" }

- 分为商品列表、商品单位、商品类别、商品颜色、商品品牌、商品形状、商品规格和商品产地等子模块，所有子模块均有增加/编辑/删除功能。
- 商品列表：描述商品信息,含新增/编辑/删除

- 新增商品：增加商品信息,输入商品完整信息，包括商品编码，选择供应商等信息,完成后点击确定按钮

![image-19](/media/img/addgoods.jpg){ loading=lazy style="max-width: 100%" }

- 编辑商品：编辑商品信息，点击编辑，修改完成后点击确定按钮

![image-20](/media/img/updategoods.jpg){ loading=lazy style="max-width: 100%" }

- 删除商品：删除商品信息，确认删除

![image-21](/media/img/delete.jpg){ loading=lazy style="max-width: 100%" }

- 商品单位：描述商品单位信息，含新增/编辑/删除
- 新增商品单位：增加商品单位信息,输入商品单位信息，完成后点击确定按钮

![image-22](/media/img/addgoodsunit.jpg){ loading=lazy style="max-width: 100%" }

- 编辑商品单位：点击编辑商品单位信息，点击编辑，修改完成后点击确定按钮

![image-23](/media/img/updategoodsunit.jpg){ loading=lazy style="max-width: 100%" }

- 删除商品单位：删除商品单位信息，确认删除

![image-24](/media/img/delete.jpg){ loading=lazy style="max-width: 100%" }

- 商品类别：描述商品类别信息，含新增/编辑/删除
- 新增商品类别：增加商品类别信息,输入商品类别信息，完成后点击确定按钮

![image-25](/media/img/addgoodscategory.jpg){ loading=lazy style="max-width: 100%" }

- 编辑商品类别：点击编辑商品类别信息，点击编辑，修改完成后点击确定按钮


![image-27](/media/img/addgoodscategory.jpg){ loading=lazy style="max-width: 100%" }

- 删除商品类别：删除商品类别信息，确认删除

![image-28](/media/img/delete.jpg){ loading=lazy style="max-width: 100%" }

- 商品颜色：描述商品颜色信息，含新增/编辑/删除
- 新增商品颜色：增加商品颜色信息,输入商品类别信息，完成后点击确定按钮

![image-29](/media/img/addgoodscolor.jpg){ loading=lazy style="max-width: 100%" }

- 编辑商品颜色：点击编辑商品颜色信息，点击编辑，修改完成后点击确定按钮
![image-30](/media/img/updategoodscolor.jpg){ loading=lazy style="max-width: 100%" }

- 删除商品颜色：删除商品颜色信息，确认删除

![image-31](/media/img/delete.jpg){ loading=lazy style="max-width: 100%" }

- 商品品牌：描述商品品牌信息，含新增/编辑/删除
- 新增商品品牌：增加商品品牌信息,输入商品品牌信息，完成后点击确定按钮

![image-32](/media/img/addgoodscategory.jpg){ loading=lazy style="max-width: 100%" }

- 编辑商品品牌：点击编辑商品品牌信息，点击编辑，修改完成后点击确定按钮

![image-33](/media/img/updategoodscategory.jpg){ loading=lazy style="max-width: 100%" }

- 删除商品品牌：删除商品品牌信息，确认删除

![image-34](/media/img/delete.jpg){ loading=lazy style="max-width: 100%" }

- 商品形状：描述商品形状信息，含新增/编辑/删除
- 新增商品形状：增加商品形状信息,输入商品形状信息，完成后点击确定按钮

![image-35](/media/img/addgoodsshape.jpg){ loading=lazy style="max-width: 100%" }
-
- 编辑商品形状：点击编辑商品形状信息，点击编辑，修改完成后点击确定按钮

![image-36](/media/img/updategoodsshape.jpg){ loading=lazy style="max-width: 100%" }

- 删除商品形状：删除商品形状信息，确认删除

![image-37](/media/img/delete.jpg){ loading=lazy style="max-width: 100%" }

- 商品规格：描述商品规格信息，含新增/编辑/删除
- 新增商品规格：增加商品规格信息,输入商品规格信息，完成后点击确定按钮

![image-38](/media/img/addgoodsspecification.jpg){ loading=lazy style="max-width: 100%" }

- 编辑商品规格：点击编辑商品规格信息，点击编辑，修改完成后点击确定按钮

![image-39](/media/img/updategoodsspecification.jpg){ loading=lazy style="max-width: 100%" }

- 删除商品规格：删除商品规格信息，确认删除

![image-40](/media/img/delete.jpg){ loading=lazy style="max-width: 100%" }

- 商品产地：描述商品产地信息，含新增/编辑/删除
- 新增商品产地：增加商品产地信息,输入商品产地信息，完成后点击确定按钮

![image-41](/media/img/addgoodsplace.jpg){ loading=lazy style="max-width: 100%" }

- 编辑商品产地：点击编辑商品产地信息，点击编辑，修改完成后点击确定按钮

![image-42](/media/img/updategoodsplace.jpg){ loading=lazy style="max-width: 100%" }

- 删除商品产地：删除商品产地信息，确认删除

![image-43](/media/img/delete.jpg){ loading=lazy style="max-width: 100%" }

#### 12. 基本管理

- 具备操作基本管理的权限可见

![image-45](/media/img/jiben.jpg){ loading=lazy style="max-width: 100%" }

- 含基本配置信息，包含公司信息、供应商信息和客户信息
- 公司信息，包含新增、编辑和删除
- 新增公司信息：输入公司名称/所在城市/地址/联系方式/负责人信息，点击确认按钮

![image-46](/media/img/company.jpg){ loading=lazy style="max-width: 100%" }

- 供应商信息，包含新增、编辑和删除
- 新增供应商信息：输入公司名称/所在城市/地址/联系方式/负责人，点击确认按钮

![image-47](/media/img/suplier.jpg){ loading=lazy style="max-width: 100%" }

- 客户信息，包含新增、编辑和删除
- 新增客户信息：输入客户名称/所在城市/地址/联系方式/负责人，点击确认按钮

![image-48](/media/img/customer.jpg){ loading=lazy style="max-width: 100%" }

#### 13. 仓库管理

- 具备操作仓库管理的权限可见
- 含仓库设置、库位设置、库位尺寸和库位属性

![image-49](/media/img/warehouse.jpg){ loading=lazy style="max-width: 100%" }

- 仓库设置,包含新增、编辑和删除
- 新增仓库：输入仓库名称/城市/地址/联系方式/负责人信息，点击确认按钮

![image-50](/media/img/addwarehouse.jpg){ loading=lazy style="max-width: 100%" }

- 库位设置,包含新增、编辑和删除
- 新增库位：输入库位名称，选择库位尺寸和库位属性，库位属性一定要选择为正常属性，才能上架，点击确认按钮

![image-51](/media/img/addplace.jpg){ loading=lazy style="max-width: 100%" }

- 库位尺寸,包含新增、编辑和删除

![image-52](/media/img/addchicun.jpg){ loading=lazy style="max-width: 100%" }

#### 14. 司机管理

- 具备操作司机管理的权限可见
- 含司机管理、提货记录
- 司机管理，包含新增、编辑和删除

![image-53](/media/img/driver.jpg){ loading=lazy style="max-width: 100%" }

- 新增司机：输入司机姓名、车牌号和联系方式信息，点击确认按钮

![image-54](/media/img/adddriver.jpg){ loading=lazy style="max-width: 100%" }

- 提货记录，显示司机与发货单的关系

![image-55](/media/img/tihuo.jpg){ loading=lazy style="max-width: 100%" }

#### 15. 上传中心

- 具备操作上传中心的权限可见
- 含初始化上传、新增上传两个子模块
- 这两个子模块都有模板下载和文件上传的功能

![image-56](/media/img/upload.jpg){ loading=lazy style="max-width: 100%" }

- 初始化上传：系统刚部署完成时用这个功能去初始化一些数据
- 新增上传：系统已有部分数据时为了不覆盖原有的数据用新增上传继续添加数据
- 模板下载：可以下载客户模板/供应商模板/商品模板，支持xlsx格式
- 文件上传：点击加号，选择相应的模板，再点确定按钮


![image-58](/media/img/fullupload.jpg){ loading=lazy style="max-width: 100%" }

#### 16. 下载中心

- 具备操作下载中心的权限可见
- 对一定时间范围内的到货通知书/发货单/库存表/库位表/商品表进行下载

![image-59](/media/img/download.jpg){ loading=lazy style="max-width: 100%" }

- 支持对一定时间范围内的到货单/发货单的详情和概况进行下载
- 下载格式为csv的

#### 17. 用户中心

- 具备操作用户中心的权限可见
- 含员工列表、验证码和员人类型


![image-61](/media/img/user.jpg){ loading=lazy style="max-width: 100%" }

- 员工列表：表示针对唯一的openid下属的所有用户的信息集合，含修改用户信息，锁定用户、删除用户
- 验证码：包括普通用户登录所必须的信息
- 员工类型：系统自带的数据，展示账户类型
