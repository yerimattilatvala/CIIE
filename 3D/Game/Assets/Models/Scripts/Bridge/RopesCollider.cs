using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RopesCollider : MonoBehaviour {

	public GameObject rope;

	void OnCollisionEnter(Collision collision){

		print ("HEY");
		if (collision.gameObject.tag == "Bullet") {
			rope.SetActive (false);
		}
	}
}
