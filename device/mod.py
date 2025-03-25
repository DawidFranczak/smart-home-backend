import socket
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from device.models import Card, Device, DeviceSettings



def add_device(data: dict, user: User):
    settings = get_object_or_404(DeviceSettings, fun=data["fun"])

    device_port: int = settings.port
    device_add_message: str = settings.message
    device_add_response: str = settings.answer

    answer = _add_device(device_add_message, device_add_response, device_port)

    if answer.get("success"):
        if user.device_set.filter(ip=answer.get("ip")).exists():
            return {"response": _("Device already exists")}, 400

        device = user.device_set.create(
            name=data["name"], fun=data["fun"], ip=answer["ip"], port=device_port
        )
        message = {
            "response": _("Successfully added device"),
            "id": device.id,
        }
        status = 201
    else:
        message = {"response": _("System failed to add the device")}
        status = 500
    return message, status


def add_uid(data: dict, user: User):
    """
    Add new rfid card to user
    """
    name = data["name"]

    try:
        sensor = user.sensor_set.get(id=data["id"])
   
        answer = _add_card(sensor.ip, sensor.port)
        print(answer)
        if answer.get("success"):
            if sensor.card_set.filter(uid=answer.get("uid")).exists():
                return {"response": _("This card is already exists.")}, 400

            card = sensor.card_set.create(uid=answer.get("uid"), name=name)
            card.save()
            return {
                "response": _("Card addes successfully."),
                "id": card.id,
            }, 201

    except:
        return {
            "response": _("System failed to add the device"),
        }, 500


# def delete_sensor(get_data: dict, user: User):
#     """
#     Delete user sensor
#     """
#     try:
#         sensor_id = str(get_data["id"])
#         if sensor_id.startswith("card"):
#             card_id = get_data["id"].split(" ")[1]
#             Card.objects.get(pk=card_id).delete()
#             response = {"response": "permission"}
#             status = 200

#         else:
#             user.sensor_set.get(id=sensor_id).delete()

#             response = {"response": "permission"}
#             status = 200

#     except Sensor.DoesNotExist or Card.DoesNotExist:
#         response = {"response": _("Sensor does not exists")}
#         status = 404
#     except:
#         response = {"response": _("Failed deleted device")}
#         status = 500

#     return (response,)


def _add_device(message: str, answer: str, port: int) -> dict:
    """
    This function searches the local network for microcontroller with
    a specific IP address range (192.168.0.2 - 192.168.0.253) and specific port.

    :params message: This is message for microcontroller (they shoud be a password)
    :params answer: This is answer from microcontroller on our message.
    :params port: This is the port under which the IP addresses will be scanned

    :return:If the microcontroller is found and its response is correct,
    the function will return a dictionary like below
    {
        "success": True,
        "ip": new_sensor_ip,
    }
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for i in range(2, 254):
        check_ip = "192.168.1." + str(i)
        print(check_ip)
        try:
            sock.sendto(bytes(message, "utf-8"), (check_ip, port))
            sock.settimeout(0.05)
            data = sock.recvfrom(128)
            response = data[0].decode("UTF-8")
            if response == answer:
                new_sensor_ip = str(data[1][0])
                sock.close()

                return {
                    "success": True,
                    "ip": new_sensor_ip,
                }

        except:
            continue

    sock.close()
    return {
        "success": False,
    }


def _add_card(ip: str, port: int) -> dict:
    """
    This function sends a command to the RFID sensor
    to add a new card and waits for a new UID.

    :params ip: This is the IP address of the RFID sensor
    :params port: This is the port of the RFID sensor

    :return: If uid read successfully return dictionary like below
    {
        "success": True,
        "uid": uid
    }
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:

        sock.sendto(str.encode("add-tag"), (ip, port))
        sock.settimeout(10)
    except TimeoutError:
        sock.close()
        return {"success": False}

    data = sock.recvfrom(128)
    uid = int(data[0].decode("UTF-8"))
    return {"success": True, "uid": uid}
