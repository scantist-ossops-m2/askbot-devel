<script>
  export let data
</script>

<h1>Welcome to Askbot</h1>

<form action="POST">
  <label>
    <span>Login name or email</span>
    <input type="text" name="login_name" />
  </label>
  <label>
    <span>Password</span>
    <input type="password" name="password" />
  </label>
  <input type="submit" value="Login" />
</form>
