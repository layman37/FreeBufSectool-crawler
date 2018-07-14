<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Sectools on Freebuf</title>
    </head>
    <?php
    function pagesCount()//返回总记录数
    {
        $coon=mysqli_connect("localhost","root","","crawler");
        $sql="select count(*) num from project";
        $r=mysqli_query($coon,$sql);
        $obj=mysqli_fetch_object($r);
        mysqli_close($coon);
        return $obj->num;
    }
    function news($pageNum,$pageSize) //返回当前页面结果
    {
        $array=array();
        $coon=mysqli_connect("localhost","root","","crawler");
        $sql="select * from project limit ".(($pageNum-1)*$pageSize).",".$pageSize;
        $r=mysqli_query($coon,$sql);
        while($obj=mysqli_fetch_object($r))
        {
            $array[]=$obj;
        }
        mysqli_close($coon);
        return $array;
    }
    @$allNum=pagesCount();
    @$pageSize=20; //每页显示多少记录
    @$pageNum=empty($_GET["pageNum"])?1:$_GET["pageNum"];
    @$endPage=ceil($allNum/$pageSize); 
    @$array=news($pageNum,$pageSize);
    ?>
    <body>
        <div class="result-title">
            <h1>
                <span class="color_h1">工具</span>
            </h1>
        </div>
        <form>
            Name:
            <input type="text" name="title">
            <input type="submit" value="搜索">
            <?php
            if(isset($_GET['title']))
            {
                $conn=mysqli_connect("localhost","root","","crawler");
                $sql="select * from project where title like '%".$_GET['title']."%'";
                $r=$conn->query($sql);
                if($r->num_rows>0)
                {
                    echo "<table border=\"1\">";
                    echo "<tbody>";
                    echo "<tr><th>Title</th><th>Description</th><th>URL</th><th>Star</th></tr>";
                    while($row=$r->fetch_assoc())
                    {
                        echo "<tr>";
                        echo "<td>".$row['title']."</td>";
                        echo "<td>".$row['description']."</td>";
                        echo "<td><a href=\"".$row['url']."\">".$row['url']."</a></td>";
                        echo "<td>".$row['star']."</td>";
                    }
                    echo "</tbody></table>";
                    echo "<hr style=\"height:5px;border:none;border-top:10px groove skyblue;\" />";
                }
                else
                {
                    echo "<p>无结果</p>";
                }
                $conn->close();
            }
            ?>
        </form>
        <div class="result-content">
            <table  class="content" border="1">
                <tbody>
                    <tr>
                        <th>Name</th>
                        <th>Description</th>
                        <th>URL</th>
                        <th>Star</th>
                    </tr>
                    <?php
                    foreach($array as $key=>$values)
                    {
                        echo "<tr>";
                        echo "<td>{$values->title}</td>";
                        echo "<td>{$values->description}</td>";
                        echo "<td><a href={$values->url}>{$values->url}</a></td>";
                        echo "<td>{$values->star}</td>";
                        echo "</tr>";
                    }
                    ?>
                </tbody>
            </table>
        </div>
        <div>
            <a href="?pageNum=1">首页</a>
            <a href="?pageNum=<?php echo $pageNum==1?1:($pageNum-1)?>">上一页</a>
            <a href="?pageNum=<?php echo $pageNum==$endPage?$endPage:($pageNum+1)?>">下一页</a>
            <a href="?pageNum=<?php echo $endPage?>">尾页</a>
        </div>

    </body>
</html>

