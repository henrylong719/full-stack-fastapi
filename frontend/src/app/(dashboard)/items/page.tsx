'use client';

import { useEffect, useMemo, useState } from 'react';
import { toast } from 'sonner';

import { ItemForm } from '@/components/common/item-form';
import { Button } from '@/components/ui/button';
import { ApiError } from '@/lib/api/client';
import {
  useCreateItemMutation,
  useDeleteItemMutation,
  useItemsQuery,
  useUpdateItemMutation,
} from '@/hooks/use-items';
import type { ItemPublic } from '@/lib/api/items';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { formatApiDetail } from '@/lib/api/errors';
import { PageHeader } from '@/components/common/page-header';

import { PaginationControls } from '@/components/common/pagination-controls';
import { usePaginationQueryParams } from '@/hooks/use-pagination-query-params';
import { EmptyState } from '@/components/common/empty-state';

import { MutationErrorAlert } from '@/components/common/mutation-error-alert';

export default function ItemsPage() {
  const { page, pageSize, setPage, setPageSize } = usePaginationQueryParams();

  const skip = (page - 1) * pageSize;
  const itemsQuery = useItemsQuery({ skip, limit: pageSize });
  const createMutation = useCreateItemMutation();
  const updateMutation = useUpdateItemMutation();
  const deleteMutation = useDeleteItemMutation();

  const [createOpen, setCreateOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<ItemPublic | null>(null);

  const [deletingItemId, setDeletingItemId] = useState<string | null>(null);

  const items = itemsQuery.data?.data ?? [];
  const totalCount = itemsQuery.data?.count ?? 0;
  const totalPages = Math.max(1, Math.ceil(totalCount / pageSize));
  const canGoPrev = page > 1;
  const canGoNext = page < totalPages;

  useEffect(() => {
    if (totalPages > 0 && page > totalPages) {
      setPage(totalPages);
    }
  }, [page, totalPages, setPage]);

  useEffect(() => {
    if (createMutation.isError) {
      toast.error('Failed to create item');
    }
  }, [createMutation.isError]);

  useEffect(() => {
    if (updateMutation.isError) {
      toast.error('Failed to update item');
    }
  }, [updateMutation.isError]);

  useEffect(() => {
    if (deleteMutation.isError) {
      toast.error('Failed to delete item');
    }
  }, [deleteMutation.isError]);

  const mutationErrorMessage = useMemo(() => {
    const err =
      createMutation.error ?? updateMutation.error ?? deleteMutation.error;
    if (!err) return null;

    if (err instanceof ApiError) {
      if (
        typeof err.body === 'object' &&
        err.body !== null &&
        'detail' in err.body
      ) {
        return formatApiDetail((err.body as { detail?: unknown }).detail);
      }
      return err.message;
    }

    return err instanceof Error ? err.message : 'Something went wrong';
  }, [createMutation.error, updateMutation.error, deleteMutation.error]);

  return (
    <div className="space-y-6">
      <PageHeader
        title="Items"
        description="Manage your items (admins will see all items)."
        action={
          <Dialog open={createOpen} onOpenChange={setCreateOpen}>
            <DialogTrigger asChild>
              <Button>Create item</Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Create item</DialogTitle>
                <DialogDescription>
                  Add a new item to your account.
                </DialogDescription>
              </DialogHeader>

              <ItemForm
                submitLabel="Create item"
                isSubmitting={createMutation.isPending}
                onSubmit={async (values) => {
                  await createMutation.mutateAsync({
                    title: values.title.trim(),
                    description: values.description?.trim() || null,
                  });
                  toast.success('Item created');
                  setCreateOpen(false);
                  setPage(1);
                }}
              />
            </DialogContent>
          </Dialog>
        }
      />

      <MutationErrorAlert
        error={createMutation.isError ? createMutation.error : null}
        fallbackMessage="Failed to create item."
      />

      <Card>
        <CardHeader>
          <CardTitle>All visible items</CardTitle>
          <CardDescription>
            Total: {itemsQuery.data?.count ?? 0}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {itemsQuery.isPending ? (
            <p>Loading items...</p>
          ) : itemsQuery.isError ? (
            <p className="text-sm text-red-600">
              Failed to load items. Please refresh or sign in again.
            </p>
          ) : items.length === 0 ? (
            <EmptyState
              title="No items yet"
              description="Create your first item to get started."
              action={
                <Button onClick={() => setCreateOpen(true)}>Create item</Button>
              }
            />
          ) : (
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Title</TableHead>
                    <TableHead>Description</TableHead>
                    <TableHead>Owner ID</TableHead>
                    <TableHead>Created</TableHead>
                    <TableHead className="w-45 text-right">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {items.map((item) => (
                    <TableRow key={item.id}>
                      <TableCell className="font-medium">
                        {item.title}
                      </TableCell>
                      <TableCell className="max-w-[320px] truncate">
                        {item.description ?? '-'}
                      </TableCell>
                      <TableCell className="max-w-55 truncate text-xs text-muted-foreground">
                        {item.owner_id}
                      </TableCell>
                      <TableCell className="text-sm text-muted-foreground">
                        {new Date(item.created_at).toLocaleString()}
                      </TableCell>
                      <TableCell>
                        <div className="flex justify-end gap-2">
                          <Dialog
                            open={editingItem?.id === item.id}
                            onOpenChange={(open) => {
                              if (!open) setEditingItem(null);
                            }}
                          >
                            <DialogTrigger asChild>
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => setEditingItem(item)}
                              >
                                Edit
                              </Button>
                            </DialogTrigger>
                            <DialogContent>
                              <DialogHeader>
                                <DialogTitle>Edit item</DialogTitle>
                                <DialogDescription>
                                  Update the selected item.
                                </DialogDescription>
                              </DialogHeader>

                              <ItemForm
                                defaultValues={{
                                  title: item.title,
                                  description: item.description ?? '',
                                }}
                                submitLabel="Save changes"
                                isSubmitting={updateMutation.isPending}
                                onSubmit={async (values) => {
                                  await updateMutation.mutateAsync({
                                    itemId: item.id,
                                    input: {
                                      title: values.title.trim(),
                                      description:
                                        values.description?.trim() || null,
                                    },
                                  });
                                  toast.success('Item updated');
                                  setEditingItem(null);
                                  setCreateOpen(false);
                                }}
                              />
                            </DialogContent>
                          </Dialog>

                          <AlertDialog>
                            <AlertDialogTrigger asChild>
                              <Button
                                variant="destructive"
                                size="sm"
                                disabled={
                                  deleteMutation.isPending ||
                                  deletingItemId === item.id
                                }
                              >
                                Delete
                              </Button>
                            </AlertDialogTrigger>
                            <AlertDialogContent>
                              <AlertDialogHeader>
                                <AlertDialogTitle>
                                  Delete item?
                                </AlertDialogTitle>
                                <AlertDialogDescription>
                                  This action cannot be undone. The item{' '}
                                  <span className="font-medium">
                                    {item.title}
                                  </span>{' '}
                                  will be permanently removed.
                                </AlertDialogDescription>
                              </AlertDialogHeader>
                              <AlertDialogFooter>
                                <AlertDialogCancel>Cancel</AlertDialogCancel>
                                <AlertDialogAction
                                  onClick={async () => {
                                    try {
                                      setDeletingItemId(item.id);
                                      await deleteMutation.mutateAsync(item.id);
                                      toast.success('Item deleted');
                                    } finally {
                                      setDeletingItemId(null);
                                    }
                                  }}
                                >
                                  {deleteMutation.isPending
                                    ? 'Deleting...'
                                    : 'Delete'}
                                </AlertDialogAction>
                              </AlertDialogFooter>
                            </AlertDialogContent>
                          </AlertDialog>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
          {!itemsQuery.isPending && !itemsQuery.isError ? (
            <PaginationControls
              page={page}
              totalPages={totalPages}
              totalCount={totalCount}
              pageSize={pageSize}
              onPageChange={setPage}
              onPageSizeChange={setPageSize}
              isDisabled={itemsQuery.isFetching}
            />
          ) : null}
        </CardContent>
      </Card>
    </div>
  );
}
