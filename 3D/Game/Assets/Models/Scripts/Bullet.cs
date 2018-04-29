using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(Rigidbody))]
public class Bullet : MonoBehaviour {

	[SerializeField]float speed;
	[SerializeField]float timeToLive;
	[SerializeField]float damage;

	void Start(){
		Camera myCamera = Camera.main;

		float x = Screen.width / 2;
		float y = Screen.height / 2;

		var ray = myCamera.ScreenPointToRay(new Vector3(x, y, 0));
		//Vector3 mousePos = Input.mousePosition;
		Ray castPoint = Camera.main.ScreenPointToRay(new Vector3(x, y, 0));
		RaycastHit hit;
		if (Physics.Raycast(castPoint, out hit, Mathf.Infinity))
		{
			this.transform.LookAt(hit.point);
		}
		Destroy (gameObject, timeToLive);
	}

	void Update(){
		transform.Translate (Vector3.forward * speed * Time.deltaTime);
	}

	void OnTriggerEnter(Collider other){
		print ("Hit " + other.name);
	}
}
