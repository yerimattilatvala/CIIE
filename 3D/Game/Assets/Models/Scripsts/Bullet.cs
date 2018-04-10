﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(Rigidbody))]
public class Bullet : MonoBehaviour {

	[SerializeField]float speed;
	[SerializeField]float timeToLive;
	[SerializeField]float damage;

	void Start(){
		Destroy (gameObject, timeToLive);
	}

	void Update(){
		transform.Translate (Vector3.left * speed * Time.deltaTime);
	}

	void OnTriggerEnter(Collider other){
		print ("Hit " + other.name);
	}
}
