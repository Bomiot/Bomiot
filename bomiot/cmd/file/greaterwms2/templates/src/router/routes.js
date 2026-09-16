
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', name: 'home', component: () => import('pages/IndexPage.vue') },
      { path: 'md/:md_docs/:lang?', component: () => import('pages/DocsReadMarkdownIt.vue') },
    ]
  },
  {
    path: '/404',
    redirect: '/'
  },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    redirect: '/'
  }
]

export default routes
