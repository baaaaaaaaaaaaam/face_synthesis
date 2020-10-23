package com.condition.umzzal.activity;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.condition.umzzal.R;
import com.condition.umzzal.adapter.VideoAdapter;
import com.condition.umzzal.object.Video;
import com.condition.umzzal.retrofit.UploadService;

import java.util.ArrayList;

import okhttp3.MediaType;
import okhttp3.RequestBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

/**
 * 영상을 고르는 activity
 *  - 영상을 고르면 VideoDetailActivity 로 화면 전환
 *      >> 이때 프로필 사진 또는 닉네임이 등록되어있지 않으면 닉네임과 프로필 사진을 받는 화면으로 이동
 */
public class VideoListActivity extends AppCompatActivity {

    String TAG="yeon["+this.getClass().getSimpleName()+"]"; // log를 위한 태그

    ArrayList<Video> videos; // 원본 영상 리스트

    RecyclerView video_list_recyclerview; // 비디오 리스트 리싸이클러뷰
    VideoAdapter videoAdapter;

    MenuItem menuItem;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_video_list);
        Log.i(TAG,"onCreate()");
        video_list_recyclerview = findViewById(R.id.video_list_recyclerview);
        video_list_recyclerview.setLayoutManager(new LinearLayoutManager(getApplicationContext()));
        videos=new ArrayList<>();
         videoAdapter = new VideoAdapter(videos,VideoListActivity.this);
        video_list_recyclerview.setAdapter(videoAdapter);
        getVideoListRequest(); // 서버에 저장된 비디오를 가지고 오기

    } // onCreate()

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        Log.d(TAG,"onCreateOptionsMenu()");
        getMenuInflater().inflate(R.menu.mypage,menu);
        menuItem=menu.findItem(R.id.my_page_icon);

        SharedPreferences profileUpload=getSharedPreferences("profileUpload", Activity.MODE_PRIVATE);
        String nickName = profileUpload.getString("nickname","f");

        if("f".equals(nickName)){ // 프로필 정보가 등록되어있지 않으면
            menuItem.setVisible(false);
        }else{ // 등록되어있으면
            menuItem.setVisible(true);
        }

        return true;
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        int id = item.getItemId();
        if(id==R.id.my_page_icon){
            Intent intent = new Intent(getApplicationContext(),MyPageActivity.class);
            intent.addFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
            startActivity(intent);
            return true;
        }else if(id==R.id.explain_icon){
            Intent intent = new Intent(getApplicationContext(),ExplainActivity.class);
            intent.addFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
            startActivity(intent);
        }
        return super.onOptionsItemSelected(item);
    }

    @Override
    protected void onResume() {
        super.onResume();
        Log.d(TAG,"onResume()");
        SharedPreferences profileUpload=getSharedPreferences("profileUpload", Activity.MODE_PRIVATE);
        String nickName = profileUpload.getString("nickname","f");

        if(menuItem!=null){
           if("f".equals(nickName)){ // 프로필 정보가 등록되어있지 않으면
            menuItem.setVisible(false);
            }else{ // 등록되어있으면
                menuItem.setVisible(true);
            }
        }

    } // onResume()

    /**
     * 서버에서 비디오 리스트를 받아오는 메소드
     */
    private void getVideoListRequest(){
        videos.clear();
        Log.i(TAG,"getVideoListRequest() 호출");
        UploadService upload= MyRetrofit2_1.getRetrofit2().create(UploadService.class);
        RequestBody mode = RequestBody.create(MediaType.parse("multipart/form-data"), "get_video_list");
        Call<Video> call = upload.get_video_list(mode);
        call.enqueue(new Callback<Video>() {
            @Override
            public void onResponse(Call<Video> call, Response<Video> response) {
               Video v=response.body();
               Log.d("test111",v.getVideo_thumbnail());
                videos.add(v);
                videoAdapter.notifyDataSetChanged();

            }

            @Override
            public void onFailure(Call<Video> call, Throwable t) {
                Log.d("test111",t.getMessage());
            }
        });


    } // getBoardRequest() 메소드

    /**
     * 비디오 리스트 정렬 메소드
     */


} // VideoListActivity class