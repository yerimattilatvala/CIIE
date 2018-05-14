using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class CameraControl : MonoBehaviour
{
    private const float Y_ANGLE_MIN = -30.0f;
    private const float Y_ANGLE_MAX = 30.0f;

    public Transform lookAt;
    public Transform camTransform;
	public Transform character;
	public AimUpDown aimUpDown;
    public float distance = 10.0f;

    private float currentX = 0.0f;
    private float currentY = 0.0f;
    private float sensitivityX = 4.0f;
    private float sensitivityY = 1.0f;

    public Texture2D crosshairImage;
    public Rect position;

    private float baseFOV;
	private bool block=false;

    private void Start()
    {
        camTransform = transform;
		baseFOV = Camera.main.fieldOfView;
    }

	public void setBlock(bool b){
		block = b;
	}

    private void Update()
    {
		if (block==false) {
			currentX += Input.GetAxis ("Mouse X");
			currentY += Input.GetAxis ("Mouse Y");

			currentY = Mathf.Clamp (currentY, Y_ANGLE_MIN, Y_ANGLE_MAX);

			if (Input.GetMouseButton (1)) {
				Camera.main.fieldOfView = 20;
            
				position = new Rect ((Screen.width - crosshairImage.width) / 2, (Screen.height - crosshairImage.height) / 2, crosshairImage.width, crosshairImage.height);

				//aimUpDown.setRotation (90f);
				character.eulerAngles = new Vector3 (character.eulerAngles.x, camTransform.eulerAngles.y, character.eulerAngles.z);
				//animator.SetFloat ("AimAngle", aimUpDown.getAngle());
				//character.transform.rotation = camTransform.transform.rotation;
			} else {
				//Puse rotar siempre por problemas a salir y entrar del apuntado
				//aimUpDown.setRotation (camTransform.rotation.x);
				character.eulerAngles = new Vector3 (character.eulerAngles.x, camTransform.eulerAngles.y, character.eulerAngles.z);

				//character.transform.rotation = camTransform.transform.rotation;
				Camera.main.fieldOfView = baseFOV;

			}
		}

    }

    private void LateUpdate()
    {
        Vector3 dir = new Vector3(0, 0, -distance);
		Quaternion rotation = Quaternion.Euler(currentY*sensitivityY, currentX*sensitivityX, 0);
        camTransform.position = lookAt.position - rotation * dir;
        camTransform.LookAt(lookAt.position);
    }

    //Dibuja la cruceta en la pantalla
    void OnGUI()
    {
		if(block==false)
        	if (Input.GetMouseButton(1))
            	GUI.Label(new Rect(Screen.width / 2 - 25, Screen.height / 2 - 25, 50, 50), crosshairImage);
    }

}
