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
  token: string,
  params?: { skip?: number; limit?: number },
) {
  const search = new URLSearchParams();
  if (params?.skip !== undefined) search.set('skip', String(params.skip));
  if (params?.limit !== undefined) search.set('limit', String(params.limit));

  const qs = search.toString();
  const path = `/api/v1/items/${qs ? `?${qs}` : ''}`;

  return apiFetch<ItemsPublic>(path, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

export function createItem(token: string, input: ItemCreateInput) {
  return apiFetch<ItemPublic>('/api/v1/items/', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      title: input.title,
      description: input.description ?? null,
    }),
  });
}

export function updateItem(
  token: string,
  itemId: string,
  input: ItemUpdateInput,
) {
  return apiFetch<ItemPublic>(`/api/v1/items/${itemId}`, {
    method: 'PATCH',
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(input),
  });
}

export function deleteItem(token: string, itemId: string) {
  return apiFetch<{ message: string }>(`/api/v1/items/${itemId}`, {
    method: 'DELETE',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}
