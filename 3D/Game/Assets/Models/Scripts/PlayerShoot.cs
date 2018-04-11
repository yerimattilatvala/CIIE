using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerShoot : MonoBehaviour {

	[SerializeField]Shooter weapon;

	void Update() {
		if (Input.GetKeyDown(KeyCode.Mouse0))
			weapon.Fire ();
	}
}
