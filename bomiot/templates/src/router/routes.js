
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', name: 'home', component: () => import('pages/IndexPage.vue') },
      { path: 'readme', component: () => import('pages/ReadMe.vue') },
      { path: 'upload', component: () => import('pages/UploadCenter.vue') },
      { path: 'doc', component: () => import('pages/DocCenter.vue') },
      { path: 'table', component: () => import('pages/TableReader.vue') },
      { path: 'user', component: () => import('pages/UserReader.vue') },
    ]
  },
  {
    path: '/404',
    component: () => import('pages/ErrorNotFound.vue')
  },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
