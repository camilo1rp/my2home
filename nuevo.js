<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.7/css/select2.min.css" rel="stylesheet"/>
    <link href="//maxcdn.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
    <script src="//maxcdn.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.min.js"></script>

    <style>
    .select2-container {
        width: 260px ! important;
    }
    .span{
        color: red;
        font-weight: bold;
    }
    .divBtn{
        text-align: center;
    }
    .contenedor{
        width: 45%;
        height: 22%;
        margin: 0 auto;
        border: solid #ccc9c9;
    }
</style>
</head>
<body>
<input id="prop" value="{{propiedad}}" hidden disabled>

<div class="container contenedor">
    <div class="row">
        <form id="formUno" method="post">
            {% csrf_token %}
            <div class="col-md-12">
                <div class="col-md-12 col-sm-12 col-xs-12">
                    <div class="col-md-12">
                        <div class="row">
                            <div class="col-md-4">
                                <label class="col-md-12 col-sm-12 col-xs-12 control-label">
                                {{form.tipo_via.label}}<span class="span"> *</span></label>
                                <div class="col-md-12">
                                    {{form.tipo_via}}
                                    <span class="help-block"></span>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <label class="col-md-12 col-sm-12 col-xs-12 control-label">
                                    {{form.via.label}}<span class="span"> *</span>
                                </label>
                                <div class="col-md-12">
                                    {{form.via}}
                                    <span class="help-block"></span>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <label class="col-md-12 col-sm-12 col-xs-12 control-label">
                                    {{form.prefijo_via.label}}<span class="span"> *</span>
                                </label>
                                <div class="col-md-12">
                                    {{form.prefijo_via}}
                                    <span class="help-block"></span>
                                </div>
                            </div>
                        </div>
                        <hr>
                        <div class="row">
                            <div class="col-md-4">
                                <div class="form-group">
                                    <label class="col-md-12 col-sm-12 col-xs-12 control-label">
                                        {{form.numero.label}}<span class="span"> *</span>
                                    </label>
                                    <div class="col-md-12">
                                        {{form.numero}}
                                        <span class="help-block"></span>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <label class="col-md-12 col-sm-12 col-xs-12 control-label">
                                    {{form.prefijo_numero.label}}<span class="span"> *</span>
                                </label>
                                <div class="col-md-12">
                                    {{form.prefijo_numero}}
                                    <span class="help-block"></span>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <label class="col-md-12 col-sm-12 col-xs-12 control-label">
                                    {{form.placa.label}}<span class="span"> *</span>
                                </label>
                                <div class="col-md-12">
                                    {{form.placa}}
                                    <span class="help-block"></span>
                                </div>
                            </div>
                        </div>
                        <hr>
                        <div class="row">
                            <div class="col-md-4">
                                <label class="col-md-12 col-sm-12 col-xs-12 control-label">
                                    {{form.barrio.label}}<span class="span"> *</span>
                                </label>
                                <div class="col-md-12">
                                    {{form.barrio}}
                                    <span class="help-block"></span>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <label class="col-md-12 col-sm-12 col-xs-12 control-label">
                                    {{form.ciudad.label}}<span class="span"> *</span>
                                </label>
                                <div class="col-md-12">
                                    {{form.ciudad}}
                                    <span class="help-block"></span>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <label class="col-md-12 col-sm-12 col-xs-12 control-label">
                                    {{form.departamento.label}}<span class="span"> *</span>
                                </label>
                                <div class="col-md-12">
                                    {{form.departamento}}
                                    <span class="help-block"></span>
                                </div>
                            </div>
                        </div>

                             {{form.propiedad}}

                        <br/>
                        <hr>
                        <div style="font-weight: bold; text-align: center;">
                            <span style="font-size: 18px;text-decoration: underline;">Direccion: </span>
                            <span id="showData"></span>
                        </div>

                        <hr>
                        <div class="row">
                            <div class="col-md-9" style="text-align: right;">
                                <span>Mostrar dirección completa en la Web ?</span>
                            </div>
                            <div class="col-md-3">
                                <div class="col-md-12">
                                    {{form.mostrar}}
                                    <span class="help-block"></span>
                                </div>
                            </div>
                        </div>
                        <br/>

                        <select id="ciudadSelect">
                              <option value="" selected>Ciudad</option>
                              <option value="0">cali</option>
                              <option value="1">Saab</option>
                              <option value="2">bogota</option>
                              <option value="3">Audi</option>
                        </select>
                        <br/>
                         <select id="deparSelect">
                              <option value="volvo" selected>Departamento</option>
                              <option value="0">cundinamarca</option>
                              <option value="1">VW</option>
                              <option value="2">Audi</option>
                              <option value="3">tres</option>
                        </select>


                        <div style="font-weight: bold; text-align: center;">
                            <span style="font-size: 18px;text-decoration: underline;">Direccion a Mostrar:</span>
                            <span id="showData2"></span>
                        </div>
                    </div>
                </div>
            </div>
            <br/>
            <div class="form-group divBtn">
                <div class="col-md-12">
                    <button type="submit" id="btnGuardar" class="btn btn-primary btnSave">
                        </i>Guardar
                    </button>
                </div>
            </div>
        </form>
    </div>
</div>


</body>
<script src="https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.7/js/select2.min.js"></script>
<script>
//SECTION 2
    $("#id_departamento").change(function(){
    var opcion = $("#id_departamento option:selected").val();
    alert("opciont "+opcion)

    $.ajax({
        url: '{% url "city:cities" %}',
        type: 'get',
        data: { 'id': opcion }
    }).done(function(data) {
        var valores = '';
        var datos = JSON.parse(data);
        $("#id_ciudad").empty();
        valores = "<option value='' selected>Seleccione Una Opción</option>"
        $.each(datos, function(item, val) {
            valores += "<option value='" + val.pk + "'>" + val.fields.name + "</option>";
        });
        $("#id_ciudad").append(valores);
    });

    });

    var propy = $("#prop").val();
    $("#id_propiedad").val(propy).change();
    $('label[for="id_propiedad"]').hide();
    $("#id_propiedad").hide()


    //Css
    $("input, select").addClass('form-control');


    $("#id_mostrar").prop('checked',true);
    $("#id_mostrar").css('height','1.5em').css('width','100%');

    if(  $("#id_mostrar").is(':checked') ){
        $("#showData2").text( $("#id_tipo_via").val()+' '+$("#id_via").val()+' '+$("#id_prefijo_via").val()+' '+$("#id_numero").val() +' # '+$("#id_prefijo_numero").val()+' - '+$("#id_placa").val()+' '+$("#id_ciudad").val()+', '+$("#id_departamento").val()+', '+$("#id_barrio").val() );
    }

    $("#id_tipo_via, #id_via, #id_prefijo_via, #id_numero, #id_prefijo_numero, #id_placa, #id_ciudad, #id_departamento, #id_barrio").keyup(function () {
        $("#showData").text( $("#id_tipo_via").val()+' '+$("#id_via").val()+' '+$("#id_prefijo_via").val()+' '+$("#id_numero").val()+' # '+$("#id_prefijo_numero").val()+' - '+$("#id_placa").val()+' '+$("#id_ciudad").val()+', '+$("#id_departamento").val()+', '+$("#id_barrio").val() );

        $("#showData2").html( $("#id_ciudad").val()+' '+$("#id_departamento").val()+' '+$("#id_barrio").val() );
        if( $("#id_mostrar").is(':checked') ){
            //Campos vacios
            if( $("#id_tipo_via").val() == '' && $("#id_via").val() == '' && $("#id_prefijo_via").val() == '' && $("#id_numero").val() == '' && $("#id_prefijo_numero").val() == '' && $("#id_placa").val() == '' && $("#id_ciudad").val() == '' && $("#id_departamento").val() == '' && $("#id_barrio").val() == '' ){
                $("#showData2").text('');
            }else{
                $("#showData2").text( $("#id_tipo_via").val()+' '+$("#id_via").val()+' '+$("#id_prefijo_via").val()+' '+$("#id_numero").val()+' # '+$("#id_prefijo_numero").val()+' - '+$("#id_placa").val()+' '+$("#id_ciudad").val()+', '+$("#id_departamento").val()+', '+$("#id_barrio").val() );
            }
        }

        //Campos vacios
        if( $("#id_tipo_via").val() == '' && $("#id_via").val() == '' && $("#id_prefijo_via").val() == '' && $("#id_numero").val() == '' && $("#id_prefijo_numero").val() == '' && $("#id_placa").val() == '' && $("#id_ciudad").val() == '' && $("#id_departamento").val() == '' && $("#id_barrio").val() == '' ){
            $("#showData").text('');
        }
    });

    $("#id_mostrar").change(function() {
        if( $("#id_mostrar").is(':checked') ){
            //Campos vacios
            if( $("#id_tipo_via").val() == '' && $("#id_via").val() == '' && $("#id_prefijo_via").val() == '' && $("#id_numero").val() == '' && $("#id_prefijo_numero").val() == '' && $("#id_placa").val() == '' && $("#id_ciudad").val() == '' && $("#id_departamento").val() == '' && $("#id_barrio").val() == '' ){
                $("#showData2").text('');
            }else{
                $("#showData2").text( $("#id_tipo_via").val()+' '+$("#id_via").val()+' '+$("#id_prefijo_via").val()+' '+$("#id_numero").val()+' # '+$("#id_prefijo_numero").val()+' - '+$("#id_placa").val()+' '+$("#id_ciudad").val()+', '+$("#id_departamento").val()+', '+$("#id_barrio").val() );
            }
        }else{
            $("#showData2").html( $("#id_ciudad").val()+' '+$("#id_departamento").val()+' '+$("#id_barrio").val() );
        }
    });




</script>
</html>