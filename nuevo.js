    function follows(id){
        $.ajax({
        url: '{% url "property:index" %}',
        type: 'get',
        data: {'prop_id': id, 'current_filters':filt, 'follow':1, 'page':page}
         }).done(function(data) {
         alert(data.command)
        if (data.command == 1) {
            alert(data.prop_id)
            console.log( $("#"+data.prop_id))
            $("#"+data.prop_id).removeClass("property-unfavorite")
            $("#"+data.prop_id).addClass("property-favorite")

        }else if(data.command == 0){
            alert(data.prop_id)
            $("#"+data.prop_id).removeClass("property-favorite")
            $("#"+data.prop_id).addClass("property-unfavorite")
        }
        else {
        window.location.href='{% url "account:login" %}'
        }
     });
     }
