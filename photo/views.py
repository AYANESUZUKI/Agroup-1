from django.shortcuts import render
#django.views.genericからTemplateViewをインポート
from django.views.generic import TemplateView
#django.views.genericからCreateViewをインポート
from django.views.generic import CreateView
#django.urlsからreverse_lazyをインポート
from django.urls import reverse_lazy
#formsモジュールからPhotoPostFormをインポート
from .forms import PhotoPostForm
#method_decoratorをインポート
from django.utils.decorators import method_decorator
#login_requiredをインポート
from django.contrib.auth.decorators import login_required

class IndexView(TemplateView):
    '''トップビューのビュー
    '''
    #index.htmlをレンダリングする
    template_name = 'index.html'

#デコレーターにより、CreatePhotoViewへのアクセスはログインユーザーに限定される
# ログイン状態でなければsetting.pyのLOGIN_URLにリダイレクトされる 
@method_decorator(login_required,name='dispatch')
class CreatePhotoView(CreateView):
  '''写真投稿のビュー

  PhotoPostFormで定義されているモデルとフィールドと連携して
  投稿データをデータベースに登録する

  Attributes:
    form_class:モデルとフィールドが登録されたフォームクラス
    template_name:レンダリングするテンプレート
    success_url:データベースへの登録完了後へのリダイレクト先
  '''
  #forms.pyのPhotoPostFormをフォームクラスとして登録
  form_class = PhotoPostForm
  #レンダリングするテンプレート
  template_name = "post_photo.html"
  #フォームデータ登録完了後のレンダリング先
  success_url = reverse_lazy('photo:post_done')

  def form_valid(self,form):
    #ファームデータの登録をここで行う 
    #commit=Falseにしてポストされたデータを取得
    postdata = form.save(commit=False)
    #投稿ユーザーのIDを取得してモデルのユーザーフィールドに格納
    postdata.user = self.request.user
    #投稿データをデータベースに登録
    postdata.save()
    #戻り値はスーパークラスのform_validの戻り値
    return super().form_valid(form)

class PostSuccessView(TemplateView):
  '''投稿完了ページのビュー

      Attributes:
        template_name:レンダリングするテンプレート
  ''' 
  #index.htmlをレンダリングする
  template_name = 'post_success.html'