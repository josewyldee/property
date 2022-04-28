
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework import status
from .bulk_insert import bulk_data_fomart
from .error_loop import fix_errors_bulk,fix_errors

class RetrieveModelMixin:
    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # print(serializer.data)
        return Response(serializer.data)

class UpdateModelMixin:
    """
    Update a model instance.
    """
    success_update='Successfully made the update'
 
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': self.success_update,
                'response': serializer.data,
            })
        else:
            error_response=fix_errors(serializer.errors)
            # error_response = fix_errors(serializer.errors.items())
            return Response({
                
                'error': error_response
            })
    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin:
    """
    Destroy a model instance.
    """
    success_delete='Data was deleted'
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
                'success': self.success_delete,
                'status':status.HTTP_204_NO_CONTENT
            })
        # return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
class ListModelMixin:
    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
class CreateModelMixin:
    success_insert='Your data has been added'
    def create(self, request, format=None, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(added_by=self.request.user)
            headers = self.get_success_headers(serializer.data)
            return Response({
                'success': self.success_insert,
                'response': serializer.data,
                'status':status.HTTP_201_CREATED,
                'headers':headers
            })
        else:
            
            # print(serializer.errors.items())
            error_response=fix_errors(serializer.errors)
            # error_response = fix_errors(serializer.errors.items())
            return Response({
                'error': error_response
            })

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
class BulkCreateModelMixin:
    success_insert='Your data has been added'

    def create(self, request, format=None, *args, **kwargs):
        bulk_data=bulk_data_fomart(request.data)
        many = isinstance(bulk_data, list)
        serializer = self.get_serializer(data=bulk_data, many=many)
        if serializer.is_valid():
            saved_user2 = serializer.save(added_by=self.request.user)
            return Response({
                'success': self.success_insert,
                'response': serializer.data[0],
            })
        else:
            error_response = fix_errors_bulk(serializer.errors)
            return Response({
                'error': error_response
            })


    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}











