'use client';

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import {
  createUser,
  deleteUser,
  getUsers,
  updateUser,
  type UserCreateInput,
  type UserUpdateInput,
} from '@/lib/api/users';

export const usersQueryKey = (params: { skip: number; limit: number }) =>
  ['users', params.skip, params.limit] as const;

export function useUsersQuery(params: { skip: number; limit: number }) {
  return useQuery({
    queryKey: usersQueryKey(params),
    queryFn: async () => {
      return getUsers(params);
    },
    retry: false,
  });
}

export function useCreateUserMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (input: UserCreateInput) => {
      return createUser(input);
    },
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
}

export function useUpdateUserMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (params: { userId: string; input: UserUpdateInput }) => {
      return updateUser(params.userId, params.input);
    },
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
}

export function useDeleteUserMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (userId: string) => {
      return deleteUser(userId);
    },
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
}
