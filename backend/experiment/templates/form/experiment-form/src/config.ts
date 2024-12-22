export const BASE_URL = 'http://localhost:8000';

export const EXPERIMENT_API_BASE_URL = `${BASE_URL}/experiment/api`;

export const createEntityUrl = (entity: string, id?: string) => {
  return id ? `${EXPERIMENT_API_BASE_URL}/${entity}/${id}/` : `${EXPERIMENT_API_BASE_URL}/${entity}/`;
}

export const createExperimentAPIUrl = (path: string) => {
  return `${EXPERIMENT_API_BASE_URL}/${path}/`;
}

export const TOKEN_URL = `${BASE_URL}/api/token/`;
