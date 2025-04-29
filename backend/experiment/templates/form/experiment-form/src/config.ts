export const BASE_URL = 'http://localhost:8000';
export const API_BASE_URL = `${BASE_URL}`;

export const EXPERIMENT_API_BASE_URL = `${BASE_URL}/experiment/api`;

export const createEntityUrl = (appName: string, entity: string, id?: string) => {
  return id ? `${API_BASE_URL}/${appName}/api/${entity}/${id}/` : `${API_BASE_URL}/${appName}/api/${entity}/`;
}

export const createExperimentEntityUrl = (entity: string, id?: string) => {
  return id ? `${EXPERIMENT_API_BASE_URL}/${entity}/${id}/` : `${EXPERIMENT_API_BASE_URL}/${entity}/`;
}

export const createExperimentAPIUrl = (path: string) => {
  return `${EXPERIMENT_API_BASE_URL}/${path}/`;
}
export const createQuestionAPIUrl = (entity: string, id?: string) => createEntityUrl('question', entity, id);

export const createQuestionQuestionAPIUrl = (entity: string, id?: string) => createQuestionAPIUrl(entity, id);

export const TOKEN_URL = `${BASE_URL}/api/token/`;
