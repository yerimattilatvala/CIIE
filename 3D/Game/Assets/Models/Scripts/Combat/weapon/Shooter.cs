using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Shooter : MonoBehaviour {

	[SerializeField]float rateOfFire;
	[SerializeField]Transform bullet;

	public Transform muzzle;

	float nextFireAllowed;
	public bool canFire;

	void Awake(){
		muzzle = transform.Find ("Muzzle");
	}

	public virtual void Fire(){
		canFire = false;

		if (Time.time < nextFireAllowed)
			return;
		nextFireAllowed = Time.time + rateOfFire;

		Instantiate (bullet, muzzle.position, muzzle.rotation);

		canFire = true;
	}
}
