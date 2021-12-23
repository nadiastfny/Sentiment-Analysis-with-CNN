<!DOCTYPE html>
<html lang="en"><!DOCTYPE html>
<head>
  <title>Analisis Sentimen</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
  <!-- Favicons -->
  <link href="static/assets/img/images.png" rel="icon">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">

    <link rel="icon" type="image/png" sizes="16x16" href="static/img/fd.jpeg"> <title>Analisis Sentimen Ulasan Produk Kecantikan </title>
    <!-- Custom fonts for this template-->
    <link href="static/vendor/fontawesome-free/css/all.min.css" rel="stylesheet" type="text/css">
    <link
        href="https://fonts.googleapis.com/css?family=Nunito:200,200i,300,300i,400,400i,600,600i,700,700i,800,800i,900,900i"
        rel="stylesheet">
    <script src="https://code.jquery.com/jquery-3.5.1.js"></script>
        <!-- <script src="https://cdn.datatables.net/1.10.24/js/jquery.dataTables.min.js"></script> -->

    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.25/css/jquery.dataTables.css">
    <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.10.25/js/jquery.dataTables.js"></script>

    <!-- Custom styles for this template-->
    <link href="static/css/sb-admin-2.min.css" rel="stylesheet">

    <style type="text/css">
        /* Penomoran otomatis pada baris */
    .css-serial {
    counter-reset: serial-number;  /* Atur penomoran ke 0 */
    }
    .css-serial td:first-child:before {
    counter-increment: serial-number;  /* Kenaikan penomoran */
    content: counter(serial-number);  /* Tampilan counter */
    }
    .card-body {
    background-color:white;
    height: auto;
    width: 100%;
    }
    .table css-serial {
    width: 100%;
    }
    </style>
</head>
<body id="page-top">
    <!-- Page Wrapper -->
<div id="wrapper">

        <!-- Sidebar -->
        <ul class="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion" id="accordionSidebar">

            <!-- Sidebar - Brand -->
            <a class="sidebar-brand d-flex align-items-center justify-content-center" href="{{ url_for('index') }}">
                <div class="sidebar-brand-icon rotate-n-15">
                    <i class="fas fa-laugh-wink"></i>
                </div>
                <div class="sidebar-brand-text mx-3">Analisis Sentimen </sup></div>
            </a>

            <!-- Divider -->
            <hr class="sidebar-divider my-0">

            <!-- Nav Item - Dashboard -->
            <li class="nav-item active">
                <a class="nav-link" href="{{ url_for('index') }}">
                    <i class="fas fa-fw fa-tachometer-alt"></i>
                    <span>Dashboard</span></a>
            </li>

            <!-- Divider -->
            <hr class="sidebar-divider">

            <!-- Heading -->
            <div class="sidebar-heading">
                Interface
            </div>

            <!-- Nav Item - Pages Collapse Menu -->
            <li class="nav-item">
                <a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#collapseTwo"
                    aria-expanded="true" aria-controls="collapseTwo">
                    <i class="fas fa-fw fa-folder"></i>
                    <span>Data</span>
                </a>
                <div id="collapseTwo" class="collapse" aria-labelledby="headingTwo" data-parent="#accordionSidebar">
                    <div class="bg-white py-2 collapse-inner rounded">
                        <!-- <h6 class="collapse-header">Jenis Data:</h6> -->
                        <a class="collapse-item" href="{{ url_for('dataAdmin') }}">Data Admin</a>
                        <a class="collapse-item" href="{{ url_for('dataCek') }}">Data Cek Review</a>
                        <a class="collapse-item" href="{{ url_for('dataPengujian') }}">Data Pengujian</a>
                        <!-- <a class="collapse-item" href="{{ url_for('dataHasilUji') }}">Hasil Data Uji</a> -->
           
                    </div>
                </div>
            </li>
            <li class="nav-item">
                <a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#collapseThree"
                    aria-expanded="true" aria-controls="collapseThree">
                    <i class="fas fa-fw fa-folder"></i>
                    <span>Master Dataset</span>
                </a>
                <div id="collapseThree" class="collapse" aria-labelledby="headingThree" data-parent="#accordionSidebar">
                    <div class="bg-white py-2 collapse-inner rounded">
                        <!-- <h6 class="collapse-header">Jenis Data:</h6> -->
                        <a class="collapse-item" href="{{ url_for('dataMaster') }}">Data Mentah</a>
                        <a class="collapse-item" href="{{ url_for('dataLatih') }}">Data Train</a>
                        <a class="collapse-item" href="{{ url_for('dataUji') }}">Data Test</a>
                    </div>
                </div>
            </li>

            <!-- Nav Item - Tables -->
            <li class="nav-item">
                <a class="nav-link" href="{{ url_for('pageKlasifikasi') }}">
                    <i class="fas fa-fw fa-table"></i>
                    <span class="collapse-item">Uji Kalimat Review</span></a>
            </li>

            <!-- Nav Item - Charts -->
            <li class="nav-item">
                <a class="nav-link" href="{{ url_for('pageUser') }}">
                    <i class="fas fa-fw fa-chart-area"></i>
                    <span>Go to website</span></a>
            </li>
            
            <!-- Divider -->
            <hr class="sidebar-divider d-none d-md-block">

            <!-- Sidebar Toggler (Sidebar) -->
            <div class="text-center d-none d-md-inline">
                <button class="rounded-circle border-0" id="sidebarToggle"></button>
            </div>
        </ul>
        <!-- End of Sidebar -->

        <!-- Content Wrapper -->
        <div id="content-wrapper" class="d-flex flex-column">
            <!-- Main Content -->
            <div id="content">
                <!-- Topbar -->
                <nav class="navbar navbar-expand navbar-light bg-white topbar mb-4 static-top shadow">
                    <!-- Sidebar Toggle (Topbar) -->
                    <button id="sidebarToggleTop" class="btn btn-link d-md-none rounded-circle mr-3">
                        <i class="fa fa-bars"></i>
                    </button>

                    <!-- Topbar Navbar -->
                    <ul class="navbar-nav ml-auto">
                        <!-- Nav Item - Search Dropdown (Visible Only XS) -->
                     
                        <div class="topbar-divider d-none d-sm-block"></div>

                        <!-- Nav Item - User Information -->
                        <li class="nav-item dropdown no-arrow">
                            <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button"
                                data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                <span class="mr-2 d-none d-lg-inline text-gray-600 small">Nadia</span>
                                <img class="img-profile rounded-circle"
                                    src="static/img/undraw_profile.svg">
                            </a>
                            <!-- Dropdown - User Information -->
                            <div class="dropdown-menu dropdown-menu-right shadow animated--grow-in"
                                aria-labelledby="userDropdown">
                                <a class="dropdown-item" href="#">
                                    <i class="fas fa-user fa-sm fa-fw mr-2 text-gray-400"></i>
                                    Profile
                                </a>
                                <div class="dropdown-divider"></div>
                                <a class="dropdown-item" href=" {{ url_for('logout') }}" >
                                    <i class="fas fa-sign-out-alt fa-sm fa-fw mr-2 text-gray-400"></i>
                                    Logout
                                </a>
                            </div>
                        </li>
                    </ul>
                </nav>
                <!-- End of Topbar -->

          <!-- Content Row -->
                    <div class="row">  
                        <ul class="breadcrumb" width="100%">
                            <!-- <li class="breadcrumb-item"><a href="{{url_for('addMaster') }}" data-toggle="modal" data-target="#addModal" >Tambah Data</a></li> -->
                            <li class="breadcrumb-item"><a href="{{ url_for('uploadFile') }}" data-toggle="modal" data-target="#myModal">Import file csv data master</a></li>
                            <li class="breadcrumb-item"><a href="/ekstrak_data">Ekstrak data master to csv</a></li>
                            <li class="breadcrumb-item"><a href="/splitdata">Split Dataset</a></li>
                        </ul>

                   
                        <div class="container"> 
                         <!-- The Modal -->
                            <div class="modal" id="myModal">
                            <div class="modal-dialog modal-lg">
                                <div class="modal-content">
                                
                                <!-- Modal Header -->
                                <div class="modal-header">
                                    <h4 class="modal-title">Import file csv </h4>
                                    <button type="button" class="close" data-dismiss="modal">&times;</button>
                                </div>
                                
                                <!-- Modal body -->
                                <div class="modal-body">
                                <form action="/import_data" enctype="multipart/form-data" method="POST">
                                    <input type="file" name="file">
                                    <input type="submit" class="btn btn-link" name="" value="Submit">
                                </form>
                                </div>                                
                                <!-- Modal footer  -->
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>
                                </div>
                                
                                </div>
                            </div>
                            </div>


                        <!-- The Modal -->
                            <div class="modal fade" id="addModal">
                                <div class="modal-dialog modal-lg modal-centered">
                                <div class="modal-content">
                                
                                    <!-- Modal Header -->
                                    <div class="modal-header">
                                    <h4 class="modal-title">Tambah Dataset</h4>
                                    <button type="button" class="close" data-dismiss="modal">&times;</button>
                                    </div>
                                    
                                    <!-- Modal body -->
                                    <div class="modal-body">
                                        <div class="chart-area">
                                            <form action="/add_data" method="POST">
                                                <p>Kalimat review : </p> 
                                                <textarea name="review" class="form-control" placeholder="Kalimat review ....." id="floatingTextarea2" style="height: 100px"></textarea><br>
                                                <p>Label : </p>
                                                <input name="label" class="form-control" placeholder="Label 1 or 0" >
                                                <p> Note : </p>
                                                    <h6>Label 1 = POSITIVE </h6>
                                                    <h6>Label 0 = NEGATIVE </h6>
                                                </p><br>
                                                <button type="submit" class="btn btn-primary">Submit</button><br>
                                            </form>
                                        </div>
                                    </div>
                                    
                                    <!-- Modal footer -->
                                    <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                                    </div>
                                    
                                </div>
                                </div>
                            </div>
  

                        </div> 
                    </div>

                <!-- Begin Page Content -->
<div class="container-fluid">
<div class="card shadow mb-4">
                                <!-- Card Header - Dropdown -->
 <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
    <h6 class="m-0 font-weight-bold text-primary">Data Master</h6>
 </div> 
<div class="card-body">
  <!-- <button type="button" class="btn btn-info btn-lg" data-toggle="modal" data-target="#myModal">Tambah Data</button><br> -->

  <table id='data' class='display' width='100%'>
    <thead>
      <tr>
        <th width="5px">No.</th>
        <th>ID</th>
        <th width="80%">Review</th>
        <th width="10%">Label</th>
        <!-- <th width="10%" colspan="2">Aksi</th> -->
      </tr>
    </thead>
</table>
        <!-- </div> -->
    </div>
</div>
</div>

   <!-- Content Row -->
</div>
<script>
            $(document).ready(function() {
                var empDataTable = $('#data').DataTable({
                    'processing': true,
                    'serverSide': true,
                    'scrollX': true,
                    'scrollY': true,
                    'paging': true,
                    'order': [[ 1, 'desc' ]],
                    'serverMethod': 'post',
                    'ajax': {
                        'url':'/master_data',
                        'type':'POST',
                        'datatype': 'json'
                    },
                    // row = empDataTable.rows().count(),
                    'pageLength': 10,
                    'lengthMenu': [[10, 20, 35, 50, -1], [10, 20, 35, 50, "All"]],
                    // "displayLength": 20,
                    searching: false,
                    sort: true,
                    "serverSide": true,
                    // data : Response.data,
                    'columns': [
                        {  
                            "data": null,
                            "class": "align-top",
                            "orderable": false,
                            "searchable": false,
                            "render": function (data, type, row, meta) {
                                return meta.row + meta.settings._iDisplayStart + 1;
                            }  
                        },
                        { 'data': 'id', "autoWidth": true, "visible": false },
                        // { 'data': 'id', "autoWidth": true, 'visible': false},
                        { 'data': 'review', "autoWidth": true},
                        { 'data': 'label',"autoWidth": true },
                        
                       ]
                    });
                });

                
            </script>


</body>
</html>
