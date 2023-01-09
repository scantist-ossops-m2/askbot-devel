import CookieParser from 'set-cookie-parser'

export async function load() {
  try {
    const resp = await fetch('http://localhost.askbot.com:8000/s/get-csrf-token/')
    const rawCookie = resp.headers.get('set-cookie')
    const cookies = CookieParser.parse(CookieParser.splitCookiesString(rawCookie))
    const csrfToken = cookies.find(cookie => cookie.name === '_csrf').value
    return { csrfToken }
  } catch (err) {
    console.log(err)
    return {}
  }
}
