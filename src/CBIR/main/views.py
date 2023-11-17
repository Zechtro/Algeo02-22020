from django.shortcuts import render, redirect
from main.forms import ImgInputForm, DatasetForm
from main.models import ImageInput, ImageDataset
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from main.static.Color_Texture.texture import cosine_similiarity, texture
from main.static.Color_Texture.color import cosine_similiarity_color, rgb_to_hsv, histogram
import shutil
import os
import time

# Create your views here.
def index_view(request):
    context = {}
    return render(request, 'index.html')
    

def upload_form_img_input(request):
    if(ImageInput.objects.all().count()!=0):
        get_object_or_404(ImageInput.objects.all()).delete()
    if (request.method == 'POST'):
        inputimage = ImageInput.objects.all()
        form = ImgInputForm(request.POST, request.FILES)
        if (form.is_valid()):
            form.save()
        else:
            context = {'form': form,
                        'inputimage': inputimage,}
            return render(request, 'inputimg.html', context)
    inputimage = ImageInput.objects.all()
    context = {'form':ImgInputForm,
               'inputimage': inputimage,}
    return render(request, 'inputimg.html',context)

def upload_form_dataset(request):
    start_delete = time.time()
    if(ImageDataset.objects.all().count()!=0):
        ImageDataset.objects.all().delete()
        abspath = os.path.abspath('media')
        shutil.rmtree(abspath+'/dataset')
    end_delete = time.time()
    print("Deleting files:", end_delete-start_delete)
    if(request.method == 'POST'):
        
        start_requestFILES = time.time()
        dataset = request.FILES.getlist('dataset')
        end_requestFILES = time.time()
        print("Request files:", end_requestFILES-start_requestFILES)
        
        start_uploadFILES = time.time()
        for img in dataset:
            if str(img).lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                ImageDataset.objects.create(image=img)
        end_uploadFILES = time.time()
        print("Upload files:", end_uploadFILES-start_uploadFILES)
    dataset = ImageDataset.objects.all()
    context = {'dataset': dataset,}
    return render(request, 'inputdataset.html',context)

def display_result(request):
    inputimage = ImageInput.objects.all()
    toggle = request.POST.get('toggle-checkbox')
    countSimilarity = 0
    
    if(toggle == 'tekstur'):
        start_search = time.time()
        
        isTekstur = True
        print("TEKSTUR")
        
        if(request.method == 'POST'):
            media_folder = os.path.abspath('media')
            
            image_folder = media_folder+'/inputimage/' 
            # print(image_folder)
            for image in os.listdir(image_folder):
                image_path = image_folder+image
                # print(image_path)
                
                V1 = texture(image_path)
            
            dataset = ImageDataset.objects.all()
            
            for image in dataset:
                dataset_path = media_folder+'/'+str(image.image)
                # print(dataset_path)
                
                V2 = texture(dataset_path)
                similarity = cosine_similiarity(V1, V2)
                if(similarity>0.6):
                    countSimilarity+=1
                # print(similarity)
                # print(image.similarity)
                image.similarity = similarity*100
                image.save()
            end_search = time.time()
            search_time = end_search-start_search
            for img in inputimage:
                img.search_time = search_time
                img.result = countSimilarity
                img.save()
    else:
        start_search = time.time()
        isTekstur = False
        print("WARNA")
        
        if(request.method == 'POST'):
        
            media_folder = os.path.abspath('media')
            
            image_folder = media_folder+'/inputimage/' 
            # print(image_folder)
            for image in os.listdir(image_folder):
                image_path = image_folder+image
                # print(image_path)
                
                hsv1 = rgb_to_hsv(image_path)
                hist1 = histogram(hsv1)
            
            dataset = ImageDataset.objects.all()
            
            for image in dataset:
                dataset_path = media_folder+'/'+str(image.image)
                # print(dataset_path)
                
                hsv2 = rgb_to_hsv(dataset_path)
                hist2 = histogram(hsv2)
                
                similarity = cosine_similiarity_color(hist1, hist2)
                if(similarity>0.6):
                    countSimilarity+=1
                # print(similarity)
                # print(image.similarity)
                image.similarity = similarity*100
                image.save()
            
            end_search = time.time()
            search_time = end_search-start_search
            for img in inputimage:
                img.search_time = search_time
                img.result = countSimilarity
                img.save()
        
    dataset = ImageDataset.objects.all().order_by('-similarity').filter(similarity__range=(60, 100))
    page = Paginator(dataset, 8)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    for img in inputimage:
        countSimilarity = img.result
        search_time = img.search_time
    search_time = round(search_time,3)
    if(countSimilarity!=0):
        if(countSimilarity%8 == 0):
            max_page = countSimilarity/8
        else:
            max_page = int(countSimilarity/8)+1
    else:
        max_page = 1
    max_page = round(max_page)
    
    print("Search time:", search_time)
    context = {'dataset':dataset,
               'inputimage':inputimage,
               'isTekstur':isTekstur,
               'page':page,
               'search_time':search_time,
               'countSimilarity':countSimilarity,
               'max_page':max_page,}
    return render(request, 'displayresult.html',context)

def change_image(request):
    if (request.method == 'POST'):
        get_object_or_404(ImageInput.objects.all()).delete()
        inputimage = ImageInput.objects.all()
        form = ImgInputForm(request.POST, request.FILES)
        if (form.is_valid()):
            form.save()
        else:
            context = {'form': form,
                        'inputimage': inputimage,}
            return render(request, 'inputimg.html', context)
    inputimage = ImageInput.objects.all()
    context = {'form':ImgInputForm,
               'inputimage': inputimage,}
    return render(request, 'changeimage.html',context)
    
def change_dataset(request):
    if(request.method == 'POST'):
        if(ImageDataset.objects.all().count()!=0):
            start_delete = time.time()
            ImageDataset.objects.all().delete()
            abspath = os.path.abspath('media')
            shutil.rmtree(abspath+'/dataset')
            end_delete = time.time()
            print("Deleting files:", end_delete-start_delete)
        start_requestFILES = time.time()
        dataset = request.FILES.getlist('dataset')
        end_requestFILES = time.time()
        print("Request files:", end_requestFILES-start_requestFILES)
        
        start_uploadFILES = time.time()
        for img in dataset:
            if str(img).lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                ImageDataset.objects.create(image=img)
        end_uploadFILES = time.time()
        print("Upload files:", end_uploadFILES-start_uploadFILES)
    dataset = ImageDataset.objects.all()
    context = {'dataset': dataset,}
    return render(request, 'changedataset.html',context)