'use client';

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { getAccessToken } from '@/lib/api/auth';
import {
  createItem,
  deleteItem,
  getItems,
  updateItem,
  type ItemCreateInput,
  type ItemUpdateInput,
} from '@/lib/api/items';

export const itemsQueryKey = (params: { skip: number; limit: number }) =>
  ['items', params.skip, params.limit] as const;

function requireToken() {
  const token = getAccessToken();
  if (!token) throw new Error('Not authenticated');
  return token;
}

export function useItemsQuery(params: { skip: number; limit: number }) {
  return useQuery({
    queryKey: itemsQueryKey(params),
    queryFn: async () => {
      const token = requireToken();
      return getItems(token, params);
    },
    retry: false,
  });
}

export function useCreateItemMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (input: ItemCreateInput) => {
      const token = requireToken();
      return createItem(token, input);
    },
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ['items'] });
    },
  });
}

export function useUpdateItemMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (params: { itemId: string; input: ItemUpdateInput }) => {
      const token = requireToken();
      return updateItem(token, params.itemId, params.input);
    },
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ['items'] });
    },
  });
}

export function useDeleteItemMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (itemId: string) => {
      const token = requireToken();
      return deleteItem(token, itemId);
    },
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ['items'] });
    },
  });
}
