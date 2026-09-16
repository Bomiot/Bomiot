# How to Add a Menu Item

## Menu Item Structure

Defined in `src/components/MenuLink.vue` `menuLinks` array:

```js
{
  tab: 'inbound',        // tab
  title: t('asn.name'),  // label (i18n)
  icon: 'download',      // icon
  link: '/asnlist'       // route
}
```

## Steps

### 1. Add Menu Item

```js
{ tab: 'inbound', title: t('asn.name'), icon: 'download', link: '/asnlist' },
```

### 2. Ensure Route Exists

In `src/router/routes.js`:

```js
{ path: 'asnlist', component: () => import('pages/inbound/ASNReader.vue') },
```

### 3. Add i18n

`zh-CN/index.js`:
```js
asn: { name: 'ASN列表' }
```

`en-US/index.js`:
```js
asn: { name: 'ASN List' }
```

## Tabs

| Tab name | Description |
|----------|-------------|
| standard | Standard (base data) |
| inbound | Inbound |
| outbound | Outbound |
| inventory | Inventory |
| docscenter | Doc Center |
| server | Server |
| basic | Basic tech |
| db | Database |
| signals | Signals |
| xxx | Development |

## Icons

Use Material Icons names, e.g. `home`, `download`. Or image icons:

```js
icon: 'img:statics/icons/asnlist.svg'
```

## Full Example

1. `MenuLink.vue`:
```js
{ tab: 'inbound', title: t('asn.name'), icon: 'download', link: '/asnlist' },
```

2. `routes.js`:
```js
{ path: 'asnlist', component: () => import('pages/inbound/ASNReader.vue') },
```

3. `zh-CN/index.js`:
```js
asn: { name: 'ASN列表' }
```

4. `en-US/index.js`:
```js
asn: { name: 'ASN List' }
```

5. `quasar build`
