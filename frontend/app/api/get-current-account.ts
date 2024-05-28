import { fetchApi } from '~/shared/api/fetch-api'

export async function getCurrentAccount() {
    const response = await fetchApi('/auth/account')
    return response.data.value?.data || null
}
