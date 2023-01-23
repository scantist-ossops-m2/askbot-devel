import { env } from '$env/dynamic/public'
import { browser } from '$app/environment'

const catalogs = {}

async function get(url, options={}) {
   options.method = 'GET'
   return await fetch(env.PUBLIC_BACKEND_URL + url, options)
}

export async function loadCatalog(languageCode) {
  if (catalogs[languageCode]) return
  const response = await get(`/i18n/?package=${env.PUBLIC_DJANGO_LOCALE_DOMAIN}&lang=${languageCode}`)
  const parsedResponse = await response.json()
  catalogs[languageCode] = parsedResponse
}

export function gettext(msgid) {
  const catalog = catalogs[env.PUBLIC_DJANGO_LANGUAGE_CODE]
  if (!catalog) return msgid
  const value = catalog.catalog[msgid]
  if (browser) console.log('have catalog', catalog)
  if (typeof value === 'string') return value
  if (typeof value === 'array') return value[0]
  return msgid
};

