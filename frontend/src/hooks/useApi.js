import { useCallback } from 'react'
import apiClient from '../services/api'

function useApi() {
  const get = useCallback(async (url, config = {}) => {
    return apiClient.get(url, config)
  }, [])

  const post = useCallback(async (url, data, config = {}) => {
    return apiClient.post(url, data, config)
  }, [])

  const patch = useCallback(async (url, data, config = {}) => {
    return apiClient.patch(url, data, config)
  }, [])

  const delete_ = useCallback(async (url, config = {}) => {
    return apiClient.delete(url, config)
  }, [])

  return { get, post, patch, delete: delete_ }
}

export default useApi
