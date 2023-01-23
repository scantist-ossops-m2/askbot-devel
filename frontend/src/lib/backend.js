import CookieParser from 'set-cookie-parser'
import { browser } from '$app/environment'
import { env } from '$env/dynamic/private'
import { env as publicEnv } from '$env/dynamic/public' 

function getBackendUrl() {
  //return browser ? publicEnv.PUBLIC_BACKEND_URL : env.publi_BACKEND_URL
  return publicEnv.PUBLIC_BACKEND_URL
}

export async function get(url, options={}) {
  options.method = 'GET'
  options.mode = 'cors'
  options.credentials = 'include'
  return await fetch(getBackendUrl() + url, options)
}

async function getBackendCookieHeader() {
  try {
    const resp = await get('/s/ping')
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
