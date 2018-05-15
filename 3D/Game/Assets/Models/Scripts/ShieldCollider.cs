using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ShieldCollider : MonoBehaviour {

	void OnCollisionEnter(Collision collision){

		print("HEY");
		if (collision.gameObject.tag == "Bullet") {
			Destroy (collision.gameObject);
		}
	}
}
