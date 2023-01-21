import CookieParser from 'set-cookie-parser'
import { env } from '$env/dynamic/private'

async function getBackendCookieHeader() {
  try {
    const headers = {'X-Requested-With': 'XMLHttpRequest'}
    const resp = await fetch('http://localhost.askbot.com:8000/s/ping/')//, {headers})
    return resp.headers.get('set-cookie')
  } catch (err) {
    return null
  }
}

export async function getAskbotCookies() {
  const cookieHeader = await getBackendCookieHeader()
  if (!cookieHeader) return null
  const splitCookies = CookieParser.splitCookiesString(cookieHeader)
  const result = {}
  for (const rawCookie of splitCookies) {
    const cookie = CookieParser.parse(rawCookie)[0]
    if (cookie.name === env.DJANGO_SESSSION_COOKIE_NAME) {
      result.sessionid = cookie
    } else if (cookie.name === env.DJANGO_CSRF_COOKIE_NAME) {
      result.csrfToken = cookie
    } else {
      result[cookie.name] = cookie
    }

  }
  return result
}
