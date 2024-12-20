import "server-only";

import { compact, isEmpty } from "lodash";
import { environment } from "src/constants/environments";
import {
  ApiRequestError,
  BadRequestError,
  ForbiddenError,
  InternalServerError,
  NetworkError,
  NotFoundError,
  RequestTimeoutError,
  ServiceUnavailableError,
  UnauthorizedError,
  ValidationError,
} from "src/errors";
import { APIResponse } from "src/types/apiResponseTypes";
import { QueryParamData } from "src/types/search/searchRequestTypes";

export type ApiMethod = "DELETE" | "GET" | "PATCH" | "POST" | "PUT";
export interface JSONRequestBody {
  [key: string]: unknown;
}

export interface HeadersDict {
  [header: string]: string;
}

// Configuration of headers to send with all requests
// Can include feature flags in child classes
export function getDefaultHeaders(): HeadersDict {
  const headers: HeadersDict = {};

  if (environment.API_AUTH_TOKEN) {
    headers["X-AUTH"] = environment.API_AUTH_TOKEN;
  }
  headers["Content-Type"] = "application/json";
  return headers;
}

/**
 * Send a request and handle the response
 */
export async function sendRequest<ResponseType extends APIResponse>(
  url: string,
  fetchOptions: RequestInit,
  queryParamData?: QueryParamData,
): Promise<ResponseType> {
  let response;
  let responseBody;
  try {
    response = await fetch(url, fetchOptions);
    responseBody = (await response.json()) as ResponseType;
  } catch (error) {
    // API most likely down, but also possibly an error setting up or sending a request
    // or parsing the response.
    throw fetchErrorToNetworkError(error, queryParamData);
  }
  if (!response.ok) {
    handleNotOkResponse(responseBody, url, queryParamData);
  }

  return responseBody;
}

export function createRequestUrl(
  method: ApiMethod,
  basePath: string,
  version: string,
  namespace: string,
  subPath = "",
  body?: JSONRequestBody,
) {
  // Remove leading slash
  const cleanedPaths = compact([basePath, version, namespace, subPath]).map(
    removeLeadingSlash,
  );
  let url = [...cleanedPaths].join("/");
  if (method === "GET" && body && !(body instanceof FormData)) {
    // Append query string to URL
    const newBody: { [key: string]: string } = {};
    Object.entries(body).forEach(([key, value]) => {
      const stringValue =
        typeof value === "string" ? value : JSON.stringify(value);
      newBody[key] = stringValue;
    });

    const params = new URLSearchParams(newBody).toString();
    url = `${url}?${params}`;
  }
  return url;
}

/**
 * Remove leading slash
 */
function removeLeadingSlash(path: string) {
  return path.replace(/^\//, "");
}

/**
 * Transform the request body into a format that fetch expects
 */
export function createRequestBody(
  payload?: JSONRequestBody,
): XMLHttpRequestBodyInit {
  if (payload instanceof FormData) {
    return payload;
  }

  return JSON.stringify(payload);
}

/**
 * Handle request errors
 */
function fetchErrorToNetworkError(
  error: unknown,
  searchInputs?: QueryParamData,
) {
  // Request failed to send or something failed while parsing the response
  // Log the JS error to support troubleshooting
  console.error(error);
  return searchInputs
    ? new NetworkError(error, searchInputs)
    : new NetworkError(error);
}

function handleNotOkResponse(
  response: APIResponse,
  url: string,
  searchInputs?: QueryParamData,
) {
  const { errors } = response;
  if (isEmpty(errors)) {
    // No detailed errors provided, throw generic error based on status code
    throwError(response, url, searchInputs);
  } else {
    if (errors) {
      const firstError = errors[0];
      throwError(response, url, searchInputs, firstError);
    }
  }
}

const throwError = (
  response: APIResponse,
  url: string,
  searchInputs?: QueryParamData,
  firstError?: unknown,
) => {
  const { status_code = 0, message = "" } = response;
  console.error(
    `API request error at ${url} (${status_code}): ${message}`,
    searchInputs,
  );

  // Include just firstError for now, we can expand this
  // If we need ValidationErrors to be more expanded
  const error = firstError ? { message, firstError } : { message };
  switch (status_code) {
    case 400:
      throw new BadRequestError(error, searchInputs);
    case 401:
      throw new UnauthorizedError(error, searchInputs);
    case 403:
      throw new ForbiddenError(error, searchInputs);
    case 404:
      throw new NotFoundError(error, searchInputs);
    case 422:
      throw new ValidationError(error, searchInputs);
    case 408:
      throw new RequestTimeoutError(error, searchInputs);
    case 500:
      throw new InternalServerError(error, searchInputs);
    case 503:
      throw new ServiceUnavailableError(error, searchInputs);
    default:
      throw new ApiRequestError(
        error,
        "APIRequestError",
        status_code,
        searchInputs,
      );
  }
};
