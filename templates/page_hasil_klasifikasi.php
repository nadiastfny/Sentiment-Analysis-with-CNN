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
                                <a class="dropdown-item" href=" {{ url_for('logout') }}">
                                    <i class="fas fa-sign-out-alt fa-sm fa-fw mr-2 text-gray-400"></i>
                                    Logout
                                </a>
                            </div>
                        </li>
                    </ul>
                </nav>
                <!-- End of Topbar -->

                <!-- Begin Page Content -->
                <div class="container-fluid">      
  <!-- Area Chart -->
                        <div class="col-xl-20 col-lg-10">
                            <div class="card shadow mb-4">
                                <div
                                    class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                                    <h6 class="m-0 font-weight-bold text-primary">Uji Text Review</h6>
                                </div>
                                <!-- Card Body -->
                                <div class="card-body">
                                           <h6> '{{ text }}' </h6>
                                            <br><br><h6>Case folding :</h6> <textarea type="text" class="form-control">{{ cfolding }} </textarea>
                                            <br><h6>Cleansing :</h6> <textarea type="text" class="form-control">{{ clean }} </textarea>
                                            <br><h6>Word Normalization :</h6>  <textarea type="text" class="form-control">{{ normalisasi }} </textarea>
                                            <br><h6>Stemming :</h6> <textarea type="text" class="form-control">{{ stem }} </textarea>
                                            <br><h6>Delete Unused Character :</h6> <textarea type="text" class="form-control">{{ unused_char }} </textarea>
                                            <br><h6>Stopword Removal :</h6> <textarea type="text" class="form-control">{{ stopword }} </textarea>
                                            <br><h6>Negation Handling :</h6> <textarea type="text" class="form-control">{{ negasi }} </textarea>
                                            <br><h6>Tokenization :</h6> <textarea type="text" class="form-control">{{ tokenisasi }} </textarea>  
                                            <br><h6> Sentiment : {{ hasil_sentimen }} </h6>
                                            <br><h6> Probabilitas : {{ sentiment_str }} </h6>
      
                                    </div>
                            </div>
                        </div>           
                </div>
                <!-- /.container-fluid -->

            </div>
            <!-- End of Main Content --> 
            <!-- Footer -->
            <footer class="sticky-footer bg-white">
                <div class="container my-auto">
                    <div class="copyright text-center my-auto">
                        <span>Copyright &copy; Wisuda 2021</span>
                    </div>
                </div>
            </footer>
            <!-- End of Footer -->

        </div>
        <!-- End of Content Wrapper -->

    </div>
    
    <!-- < Scroll to Top Button-->
    <a class="scroll-to-top rounded" href="#page-top">
        <i class="fas fa-angle-up"></i>
    </a>
    <!-- Bootstrap core JavaScript-->
    <script src="static/vendor/jquery/jquery.min.js"></script>
    <script src="static/vendor/bootstrap/js/bootstrap.bundle.min.js"></script>
    <!-- Core plugin JavaScript-->
    <script src="static/vendor/jquery-easing/jquery.easing.min.js"></script>
    <!-- Custom scripts for all pages-->
    <script src="static/js/sb-admin-2.min.js"></script>
    <!-- Page level plugins -->
    <script src="static/vendor/chart.js/Chart.min.js"></script>
    <!-- Page level custom scripts -->
    <script src="static/js/demo/chart-area-demo.js"></script>
    <script src="static/js/demo/chart-pie-demo.js"></script>
</body>
</html>