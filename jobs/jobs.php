<?php
$host = (empty($_SERVER['HTTPS']) ? 'http' : 'https') . "://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]";

$url = "https://efg79w6sf2.execute-api.us-east-1.amazonaws.com/dev/helper/login/";

$curl = curl_init();
curl_setopt($curl, CURLOPT_URL, $url);
curl_setopt($curl, CURLOPT_POST, true);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);

$headers = array(
   "Accept: application/json",
   "Content-Type: application/json",
   'language: PT-BR',
    'token_api: am9iZmlzaGluZw=='
);
curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);

$data = <<<DATA
{
  "email": "helper@jobfishing.com",
  "password": "helper1"
}
DATA;

curl_setopt($curl, CURLOPT_POSTFIELDS, $data);

$resp = curl_exec($curl);
$respEncoded = json_decode($resp);
$token = $respEncoded->token;
curl_close($curl);

if ($token) {
    $company = $_GET['company'];
    $job = $_GET['job'];
    $urlJob = 'https://efg79w6sf2.execute-api.us-east-1.amazonaws.com/dev/company/'.$company.'/job/'.$job;

    $cURLConnection = curl_init();

    curl_setopt($cURLConnection, CURLOPT_URL, $urlJob);
    curl_setopt($cURLConnection, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($cURLConnection, CURLOPT_HTTPHEADER, array(
        "Accept: application/json",
        "Content-Type: application/json",
        'language: PT-BR',
        'token_api: am9iZmlzaGluZw==',
        'authorization: Bearer '.$token
    ));
    $phoneList = curl_exec($cURLConnection);
    curl_close($cURLConnection);
    // print_r($phoneList);
    $jsonArrayResponse = json_decode($phoneList);
    $job = $jsonArrayResponse->job;
}

?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Fishing</title>
</head>

<body style="font-family: Arial, Helvetica, sans-serif; color: #000; margin: 0 auto; padding: 0;
background-color: #fff; max-width: 100%; text-align: center;">

<main style="max-width: 780px; margin: 0 auto; padding: 0 20px 100px 20px;">
    <header style="border-bottom: 1px solid #E3E3E3; padding: 0 0 30px 0;">
        <div>
            <img style=" max-width: 100%; margin: 40px 0; width: 200px;" src="./img/banner-top.png" alt="">
        </div>
        <div style="display: flex; justify-content: space-between;">
            <div style="display: flex;">
                <!-- <div
                    style="width: 138px; height: 141px; background-color: #f1f2f3; border-radius: 30px; display: flex; align-items: center;padding:0; margin-right:20px;">
                    <div style="margin: 0 auto;">
                        <img src="./img/imagem.png" alt="">
                    </div>
                </div> -->
                <div style="text-align: left; line-height: 0.7;">
                    <h5 style="color: #1373FA;font-size: 22px;font-weight: bold; margin: 40px auto 0;"><?php echo $job->company->name; ?></h5>
                    <p style="font-size: 18px;color: #262626;font-weight: bold;"><?php
                        echo $job->city .', '. $job->state_code;
                    ?></p>
                </div>
            </div>
            
            <div style="width: 132px; height: 44px; margin-top: 50px;">
                <a href='https://www.facebook.com/sharer/sharer.php?u=<?php echo $host; ?>&t=<?php echo 'Dá uma conferida na vaga que encontrei no Jobfishing!'; ?>'
   onclick="javascript:window.open(this.href, '', 'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=300,width=600');return false;"
   target="_blank" title="Share on Facebook">
   <img src="./img/facebook.png" alt="">
</a>
            </div>
        </div>
    </header>
    <section>
        
        <div style="display: flex;justify-content: space-evenly;">
            <p style="font-size: 16px;font-weight: bold;color: #5c5c5c;"> <span style="color: #000;"><?php echo $job->positions_filled; ?> de <?php echo $job->number_positions; ?></span>
                vagas preenchidas</p>
            <p style="color: #5c5c5c;">Expira em: <strong style="color: #000;"><?php 
            $expiresIn = explode('-', explode('T', $job->expires_in)[0]);
            echo $expiresIn[2].'/'.$expiresIn[1].'/'.$expiresIn[0];
 ?></strong></p>
 <p>De $<?php echo $job->rate ?> até $<?php echo $job->rate_max ?> <?php echo $job->type_rate == 'H' ? '/h': '/dia'  ?></p>
        </div>
        <div style="text-align: left; color: #5c5c5c; ">
        <div style="margin-top: 80px;">
                <h2 style="font-size: 29px;font-weight: bold;">JOB</h2>
                <p style="font-size: 16px;font-weight: bold;"><?php echo $job->labor ? "Labor" : $job->skills; ?></p>
            </div>

            <div style="margin: 80px auto;">
                <h2 style="font-size: 29px;font-weight: bold;">Descrição</h2>
                <p style="color: #5c5c5c;">Data de início: <strong style="color: #000;"><?php 
            $expiresIn = explode('-', explode('T', $job->date_start)[0]);
            echo $expiresIn[2].'/'.$expiresIn[1].'/'.$expiresIn[0];
 ?></strong></p>
 <p style="color: #5c5c5c;">Data de término: <strong style="color: #000;"><?php 
            $expiresIn = explode('-', explode('T', $job->date_end)[0]);
            echo $expiresIn[2].'/'.$expiresIn[1].'/'.$expiresIn[0];
 ?></strong></p>
 <p style="color: #5c5c5c;">Horário: <strong style="color: #000;"><?php 
            echo $job->time_start.' às '.$job->time_end;
 ?></strong></p>
 <p style="color: #5c5c5c;">Precisa de carro? <strong style="color: #000;"><?php 
            echo $job->car_required ? 'Sim': 'Não';
 ?></strong></p>
 <p style="color: #5c5c5c;">Precisa de habilitação? <strong style="color: #000;"><?php 
            echo $job->driver_license ? 'Sim': 'Não';
 ?></strong></p>
 <p style="color: #5c5c5c;">Pode ser contratado ao final do job? <strong style="color: #000;"><?php 
            echo $job->hire ? 'Sim': 'Não';
 ?></strong></p>
            </div>
            
                   <?php
                    $languages = $job->languages;

                    if(count($languages)){
echo '<div style="margin: 40px auto;">
                <h2 style="font-size: 29px;font-weight: bold;">Linguagem obrigatória</h2>
            </div>
            <div style="margin: 40px auto;font-size: 16px;font-weight: bold;">';
                    }

                    for ($i=0; $i < count($languages); $i++) { 
                        echo '<p style="margin: 0 0 10px 0; color: #5c5c5c;"> '.$languages[$i]->name.' ('.$languages[$i]->level->value.')</p>';
                    }

                    if(count($languages)){
                        echo '</div>';
                    }

                    
                   ?>
                
        
            
        </div>
    </section>
</main>
    
</body>

</html>