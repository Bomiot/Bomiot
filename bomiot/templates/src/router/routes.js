
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', name: 'home', component: () => import('pages/IndexPage.vue') },
      { path: 'readme', component: () => import('pages/basic/READMEReader.vue') },
      { path: 'upload', component: () => import('pages/UploadCenter.vue') },
      { path: 'doc', component: () => import('pages/DocCenter.vue') },
      { path: 'table', component: () => import('pages/TableReader.vue') },
      { path: 'user', component: () => import('pages/UserReader.vue') },
      { path: 'team', component: () => import('pages/TeamReader.vue') },
      { path: 'department', component: () => import('pages/DepartmentReader.vue') },
      { path: 'pypi', component: () => import('pages/PyPiReader.vue') },
      { path: 'pypicharts', component: () => import('pages/PyPiCharts.vue') },
      { path: 'pid', component: () => import('pages/PIDReader.vue') },
      { path: 'cpu', component: () => import('pages/CPUReader.vue') },
      { path: 'memory', component: () => import('pages/MemoryReader.vue') },
      { path: 'disk', component: () => import('pages/DiskReader.vue') },
      { path: 'network', component: () => import('pages/NetworkReader.vue') },
      { path: 'serverecharts', component: () => import('pages/ServerEcharts.vue') },
      { path: 'pidcharts', component: () => import('pages/PIDCharts.vue') },
      { path: 'api', component: () => import('pages/APIReader.vue') },
      { path: 'example', component: () => import('pages/ExampleReader.vue') },
      { path: 'locust', component: () => import('pages/basic/LocustReader.vue') },
      { path: 'poetry', component: () => import('pages/basic/PoetryReader.vue') },
      { path: 'supervisor', component: () => import('pages/basic/SupervisorReader.vue') },
      { path: 'sqlite', component: () => import('pages/db/SqliteReader.vue') },
      { path: 'mysql', component: () => import('pages/db/MysqlReader.vue') },
      { path: 'postgresql', component: () => import('pages/db/PostgresqlReader.vue') },
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
