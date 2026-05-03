import { apiFetch } from './client';

export type ItemPublic = {
  id: string;
  title: string;
  description: string | null;
  owner_id: string;
  created_at: string;
};

export type ItemsPublic = {
  data: ItemPublic[];
  count: number;
};

export type ItemCreateInput = {
  title: string;
  description?: string | null;
};

export type ItemUpdateInput = {
  title?: string;
  description?: string | null;
};

export function getItems(
  params?: { skip?: number; limit?: number },
  token?: string,
) {
  const search = new URLSearchParams();
  if (params?.skip !== undefined) search.set('skip', String(params.skip));
  if (params?.limit !== undefined) search.set('limit', String(params.limit));

  const qs = search.toString();
  const path = `/api/v1/items/${qs ? `?${qs}` : ''}`;

  return apiFetch<ItemsPublic>(path, {
    method: 'GET',
    token,
  });
}

export function createItem(input: ItemCreateInput, token?: string) {
  return apiFetch<ItemPublic>('/api/v1/items/', {
    method: 'POST',
    token,
    body: JSON.stringify({
      title: input.title,
      description: input.description ?? null,
    }),
  });
}

export function updateItem(
  itemId: string,
  input: ItemUpdateInput,
  token?: string,
) {
  return apiFetch<ItemPublic>(`/api/v1/items/${itemId}`, {
    method: 'PATCH',
    token,
    body: JSON.stringify(input),
  });
}

export function deleteItem(itemId: string, token?: string) {
  return apiFetch<{ message: string }>(`/api/v1/items/${itemId}`, {
    method: 'DELETE',
    token,
  });
}
