﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraControl : MonoBehaviour
{
    private const float Y_ANGLE_MIN = -30.0f;
    private const float Y_ANGLE_MAX = 50.0f;

    public Transform lookAt;
    public Transform camTransform;
    public float distance = 10.0f;

    private float currentX = 0.0f;
    private float currentY = 0.0f;
    private float sensitivityX = 4.0f;
    private float sensitivityY = 1.0f;

	private float baseFOV;

    private void Start()
    {
        camTransform = transform;
		baseFOV = Camera.main.fieldOfView;
    }

    private void Update()
    {
        currentX += Input.GetAxis("Mouse X");
        currentY += Input.GetAxis("Mouse Y");

        currentY = Mathf.Clamp(currentY, Y_ANGLE_MIN, Y_ANGLE_MAX);

		if (Input.GetMouseButton(1))
			Camera.main.fieldOfView = 10;
		else 
			Camera.main.fieldOfView = baseFOV;
    }

    private void LateUpdate()
    {
        Vector3 dir = new Vector3(0, 0, -distance);
		Quaternion rotation = Quaternion.Euler(currentY*sensitivityY, currentX*sensitivityX, 0);
        camTransform.position = lookAt.position - rotation * dir;
        camTransform.LookAt(lookAt.position);
    }

}
