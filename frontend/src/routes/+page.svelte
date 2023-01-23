<script>
  import { gettext } from '$lib/i18n'
  export let data
  const ngettext = (str, str2, num) => num === 1 ? str : str2
  const rnd = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min
</script>

<h1>Welcome { ngettext('user', 'users', rnd(1, 20)) }</h1>
<a href="/page_two">Page Two</a>

<form action="POST">
  <label>
    <span>{ gettext('Login name or email') }</span>
    <input type="text" name="login_name" />
  </label>
  <label>
    <span>{ gettext('Password') }</span>
    <input type="password" name="password" />
  </label>
  <input type="submit" value="Login" />
</form>
