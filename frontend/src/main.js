import { mount } from 'svelte'
import './app.css'
import 'bootstrap/dist/css/bootstrap.min.css' //bootstrap 적용
import 'bootstrap/dist/js/bootstrap.min.js'//bootstrap 적용
import App from './App.svelte'

const app = mount(App, {
  target: document.getElementById('app'),
})

export default app
