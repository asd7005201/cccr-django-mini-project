from django.shortcuts import redirect, render
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from .models import Photo
from django.http import HttpResponseRedirect
from django.contrib import messages

class PhotoList(ListView):
    model = Photo
    template_name_suffix = '_list'

class PhotoCreate(CreateView):
    model =Photo
    fields = ['author', 'text', 'image']
    template_name_suffix = '_create'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            #올바르다면
            # form : 모델폼
            form.instance.save()
            return redirect('/')
        else:
            #올바르지 않다면
            return self.render_to_response({'form':form})    

class PhotoUpdate(UpdateView):
    model = Photo
    fields = ['author', 'text', 'image']
    template_name_suffix = '_update'
    # success_url = '/'

    def dispatch(self, request, *arg, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            message.warning(request, '수정 권한이 없습니다.')
            return HttpResponseRedirect('/')

        else:
            return super(PhotoUpdate, self).dispatch(request, *arg, **kwargs)


class PhotoDelete(DeleteView):
    model = Photo
    template_name_suffix = '_delete'
    success_url = '/'

    def dispatch(self, request, *arg, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            message.warning(request, '삭제 권한이 없습니다.')
            return HttpResponseRedirect('/')
        else:
            return super(PhotoDelete, self).dispatch(request, *arg, **kwargs)

class PhotoDetail(DetailView):
    model = Photo
    template_name_suffix = '_detail'