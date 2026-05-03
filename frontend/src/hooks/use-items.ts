'use client';

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

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

export function useItemsQuery(params: { skip: number; limit: number }) {
  return useQuery({
    queryKey: itemsQueryKey(params),
    queryFn: async () => {
      return getItems(params);
    },
    retry: false,
  });
}

export function useCreateItemMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (input: ItemCreateInput) => {
      return createItem(input);
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
      return updateItem(params.itemId, params.input);
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
      return deleteItem(itemId);
    },
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ['items'] });
    },
  });
}
