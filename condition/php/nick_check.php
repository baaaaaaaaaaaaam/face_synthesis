<?php
	$db_host="localhost";
	$db_user="ansgyqja";
	$db_password="akwldrk1";
	$db_name="umzzal";
	$con=mysqli_connect($db_host,$db_user,$db_password,$db_name);
	if(!$con){ die("연결 실패 : ".mysqli_connect_error()); }


	
	//비디오 리스트받아가기 
	if(($_POST['mode'])=='get_video_list'){
		$videos=[];
		$videos1=[];
		$sql = "SELECT * FROM videoList";
		$result = mysqli_query($con,$sql);
		if(mysqli_num_rows($result)>0){
			
			while($videos = mysqli_fetch_array($result)){
				    $video_no = $videos['video_no'];
					$video_name = $videos['video_name'];
					$video_thumbnail = $videos['video_thumbnail'];
					$video_route = $videos['video_route'];
					$video = ['video_no'=>$video_no,'video_name'=>$video_name,'video_thumbnail'=>$video_thumbnail,'video_route'=>$video_route];
					// array_push($videos1,$video);
			}
		echo json_encode($video);
	}
	}else{
	//아이디 중복체크
		$id = $_POST['id'];
		$sql = "SELECT * FROM member WHERE member_id='$id'";
		$result = mysqli_query($con,$sql);
		$count = mysqli_num_rows($result);
	   if($count>0){
		echo json_encode( ['id' => 'old'] );
	   }else{
		if (!mysqli_query($con, "INSERT INTO member (member_id) VALUES ('$id');")) {
			echo "회원가입 실패 (Error: ".mysqli_error($con).")";
		}else{
			echo json_encode( ['id' => 'new'] );
		}
	}
   }

?>
