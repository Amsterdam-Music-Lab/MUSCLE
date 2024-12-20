export const BASE_URL = 'http://localhost:8000/experiment/api';

export const createEntityUrl = (entity: string, id?: string) => {
  return id ? `${BASE_URL}/${entity}/${id}/` : `${BASE_URL}/${entity}/`;
}

export const createApiUrl = (path: string) => {
  return `${BASE_URL}/${path}/`;
}
