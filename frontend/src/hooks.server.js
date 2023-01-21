import CookieParser from 'set-cookie-parser'
import { getAskbotCookies } from '$lib/backend'

function setCookieToEvent(event, cookie) {
  if (!cookie) return
  event.cookies.set(cookie.name, cookie.value, {
    httpOnly: false,
    secure: cookie.secure,
    sameSite: cookie.sameSite,
    maxAge: cookie.maxAge,
    expires: cookie.expires,
    path: cookie.path
  })
}

export async function handle({ event, resolve }) {
  const sessionid = event.cookies.get('sessionid')
  const csrfToken = event.cookies.get('_csrf')
  if (!(sessionid && csrfToken)) {
    const askbotCookies = await getAskbotCookies()
    if (askbotCookies) {
      setCookieToEvent(event, askbotCookies.sessionid)
      setCookieToEvent(event, askbotCookies.csrfToken)
    }
  }
  return resolve(event)
}
