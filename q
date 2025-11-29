[1mdiff --git a/event/views.py b/event/views.py[m
[1mindex b76c16e..10f302b 100644[m
[1m--- a/event/views.py[m
[1m+++ b/event/views.py[m
[36m@@ -63,8 +63,10 @@[m [mclass GetActionsAndEvents(APIView):[m
         id = request.query_params.get("id")[m
         fun = request.query_params.get("fun")[m
         models = get_models_with_supported_actions(request.user)[m
[32m+[m[32m        print(models)[m[41m[m
         register = DeviceRegistry()[m
         model = register.get_model(fun)[m
[32m+[m[32m        print(model)[m[41m[m
         device = get_object_or_404(model, home__users=request.user, pk=id)[m
         return Response([m
             {[m
[36m@@ -103,6 +105,8 @@[m [mclass TriggerEvent(APIView):[m
             return Response({}, HTTP_400_BAD_REQUEST)[m
         device = get_object_or_404(Device, pk=device_id)[m
         events = device.events.filter(event=event_type)[m
[32m+[m[32m        dm = DeviceMessenger()[m[41m[m
         for event in events:[m
[31m-            DeviceMessenger().send(device.get_router_mac(), get_event_request(event))[m
[32m+[m[32m            print(get_event_request(event))[m[41m[m
[32m+[m[32m            dm.send(device.get_router_mac(), get_event_request(event))[m[41m[m
         return Response({}, HTTP_200_OK)[m
