import { loadCatalog } from '$lib/i18n'
import { env } from '$env/dynamic/public'

export async function load() {
  await loadCatalog(env.PUBLIC_DJANGO_LANGUAGE_CODE)
  return {}
}
