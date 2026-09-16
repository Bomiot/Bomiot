# 如何新增一个菜单项

## 菜单项结构

菜单项定义在 `src/components/MenuLink.vue` 的 `menuLinks` 数组中，每项结构：

```js
{
  tab: 'inbound',        // 所属 Tab
  title: t('asn.name'),  // 显示标题（i18n）
  icon: 'download',      // 图标（Material Icons）
  link: '/asnlist'       // 路由路径
}
```

## 步骤

### 1. 在 MenuLink 添加菜单项

```js
{ tab: 'inbound', title: t('asn.name'), icon: 'download', link: '/asnlist' },
```

### 2. 确保路由已注册

在 `src/router/routes.js` 中确认对应路由存在：

```js
{ path: 'asnlist', component: () => import('pages/inbound/ASNReader.vue') },
```

### 3. 添加 i18n 翻译

`src/i18n/zh-CN/index.js`：

```js
asn: { name: 'ASN列表', detail: 'ASN明细' }
```

`src/i18n/en-US/index.js`：

```js
asn: { name: 'ASN List', detail: 'ASN Detail' }
```

## Tab 分类

菜单项通过 `tab` 字段归属到不同 Tab。现有 Tab：

| Tab name | 说明 |
|----------|------|
| standard | 标准（基础数据） |
| inbound | 入库 |
| outbound | 出库 |
| inventory | 库存 |
| docscenter | 文档中心 |
| server | 服务器 |
| basic | 基础技术 |
| db | 数据库 |
| signals | 信号 |
| xxx | 开发 |

## 图标

使用 Material Icons 名称，如 `home`、`download`、`storage`。也支持图片图标：

```js
icon: 'img:statics/icons/asnlist.svg'
```

## 完整示例：新增入库菜单

1. `MenuLink.vue`：
```js
{ tab: 'inbound', title: t('asn.name'), icon: 'download', link: '/asnlist' },
```

2. `routes.js`：
```js
{ path: 'asnlist', component: () => import('pages/inbound/ASNReader.vue') },
```

3. `zh-CN/index.js`：
```js
asn: { name: 'ASN列表' }
```

4. `en-US/index.js`：
```js
asn: { name: 'ASN List' }
```

5. `quasar build` 验证
