using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerShoot : MonoBehaviour {
	private bool block = false;
	[SerializeField]Shooter weapon;
	private CharacterStats stats;

	void Start(){
		stats = GetComponent<CharacterStats> ();
	}

	public void setBlock(bool b){
		block = b;
	}

	void Update() {
		if (block == false) {
			if (stats.isDead () == false) {
				if (Input.GetKeyDown (KeyCode.Mouse0))
					weapon.Fire ();
			}
		}
	}
}
