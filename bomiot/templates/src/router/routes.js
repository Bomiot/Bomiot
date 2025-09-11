
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', name: 'home', component: () => import('pages/IndexPage.vue') },
      { path: 'upload', component: () => import('pages/UploadCenter.vue') },
      { path: 'doc', component: () => import('pages/DocCenter.vue') },
      { path: 'table', component: () => import('pages/TableReader.vue') },
      { path: 'user', component: () => import('pages/UserReader.vue') },
      { path: 'team', component: () => import('pages/TeamReader.vue') },
      { path: 'department', component: () => import('pages/DepartmentReader.vue') },
      { path: 'pid', component: () => import('pages/PIDReader.vue') },
      { path: 'cpu', component: () => import('pages/CPUReader.vue') },
      { path: 'memory', component: () => import('pages/MemoryReader.vue') },
      { path: 'disk', component: () => import('pages/DiskReader.vue') },
      { path: 'network', component: () => import('pages/NetworkReader.vue') },
      { path: 'serverecharts', component: () => import('pages/ServerEcharts.vue') },
      { path: 'pidcharts', component: () => import('pages/PIDCharts.vue') },
      { path: 'inscription', component: () => import('pages/basic/InscriptionReader.vue') },
      { path: 'readme', component: () => import('pages/basic/READMEReader.vue') },
      { path: 'locust', component: () => import('pages/basic/LocustReader.vue') },
      { path: 'poetry', component: () => import('pages/basic/PoetryReader.vue') },
      { path: 'supervisor', component: () => import('pages/basic/SupervisorReader.vue') },
      { path: 'setup', component: () => import('pages/basic/SetupReader.vue') },
      { path: 'bomiotconf', component: () => import('pages/basic/BomiotconfReader.vue') },
      { path: 'terminal', component: () => import('pages/basic/TerminalReader.vue') },
      { path: 'django', component: () => import('pages/basic/DjangoReader.vue') },
      { path: 'flask', component: () => import('pages/basic/FlaskReader.vue') },
      { path: 'fastapi', component: () => import('pages/basic/FastapiReader.vue') },
      { path: 'structure', component: () => import('pages/db/StructureReader.vue') },
      { path: 'sqlite', component: () => import('pages/db/SqliteReader.vue') },
      { path: 'mysql', component: () => import('pages/db/MysqlReader.vue') },
      { path: 'postgresql', component: () => import('pages/db/PostgresqlReader.vue') },
      { path: 'permission', component: () => import('pages/signals/PermissionReader.vue') },
      { path: 'scheduler', component: () => import('pages/signals/SchedulerReader.vue') },
      { path: 'observer', component: () => import('pages/signals/ObserverReader.vue') },
      { path: 'server', component: () => import('pages/signals/ServerReader.vue') },
      { path: 'data', component: () => import('pages/signals/DataReader.vue') },
      { path: 'example', component: () => import('pages/signals/ExampleReader.vue') },
      { path: 'interaction', component: () => import('pages/signals/InteractionReader.vue') },
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
