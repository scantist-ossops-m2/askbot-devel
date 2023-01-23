import { getAskbotCookies } from '$lib/backend'
import { loadCatalog } from '$lib/i18n'
import { env } from '$env/dynamic/public'

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
  //todo: here we have an opportunity to handle the url-based language selection
  await loadCatalog(env.PUBLIC_DJANGO_LANGUAGE_CODE)
  return resolve(event)
}
