import { boot } from 'quasar/wrappers'
import { Notify } from 'quasar';

const position = 'right';
const progress = true;
const multiLine = true;
const group = true;
const classes = 'flat';
const timeout = 3000;

export default boot(async (/* { app, router, ... } */) => {
  Notify.registerType('success', {
    icon: 'check_circle',
    position: position,
    progress: progress,
    multiLine: multiLine,
    group: group,
    color: 'positive',
    textColor: 'black',
    classes: classes,
    timeout: timeout
  })
  Notify.registerType('error', {
    icon: 'warning',
    position: position,
    progress: progress,
    multiLine: multiLine,
    group: group,
    color: 'negative',
    textColor: 'white',
    classes: classes,
    timeout: timeout
  })
    Notify.registerType('warning', {
    icon: 'privacy_tip',
    position: position,
    progress: progress,
    multiLine: multiLine,
    group: group,
    color: 'warning',
    textColor: 'black',
    classes: classes,
    timeout: timeout
  })
    Notify.registerType('info', {
    icon: 'privacy_tip',
    position: position,
    progress: progress,
    multiLine: multiLine,
    group: group,
    color: 'info',
    textColor: 'black',
    classes: classes,
    timeout: timeout
  })
})
