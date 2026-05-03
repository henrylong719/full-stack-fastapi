'use client';

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { loginAccessToken } from '@/lib/api/login';
import {
  changeMyPassword,
  getCurrentUser,
  updateMe,
  type ChangeMyPasswordInput,
  type UpdateMeInput,
} from '@/lib/api/users';

import { logoutAccessToken } from '@/lib/api/auth';
import { ApiError } from '@/lib/api/client';

export function isAuthError(error: unknown): boolean {
  return error instanceof ApiError && (error.status === 401 || error.status === 403);
}

export function useLoginMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: loginAccessToken,
    onSuccess: async (data) => {
      try {
        const user = await getCurrentUser(data.access_token);
        queryClient.setQueryData(['auth', 'me'], user);
      } catch {
        await queryClient.invalidateQueries({ queryKey: ['auth', 'me'] });
      }
    },
  });
}

export function useCurrentUserQuery(options?: { enabled?: boolean }) {
  return useQuery({
    queryKey: ['auth', 'me'],
    queryFn: async () => {
      return getCurrentUser();
    },
    enabled: options?.enabled ?? true,
    retry: false,
  });
}

export function useLogoutMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: logoutAccessToken,
    onSettled: () => {
      queryClient.clear();
    },
  });
}

export function useUpdateMeMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (input: UpdateMeInput) => {
      return updateMe(input);
    },
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ['auth', 'me'] });
    },
  });
}

export function useChangeMyPasswordMutation() {
  return useMutation({
    mutationFn: async (input: ChangeMyPasswordInput) => {
      return changeMyPassword(input);
    },
  });
}
