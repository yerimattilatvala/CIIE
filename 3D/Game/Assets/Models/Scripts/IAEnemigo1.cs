using System;
using UnityEngine;

	[RequireComponent(typeof (UnityEngine.AI.NavMeshAgent))]
	[RequireComponent(typeof (Enemy1Character))]
	public class IAEnemigo1 : MonoBehaviour
	{
		public UnityEngine.AI.NavMeshAgent agent { get; private set; }             // the navmesh agent required for the path finding
		public Enemy1Character character { get; private set; } // the character we are controlling
		public Transform target;                                    // target to aim for
        public float lookRadius = 15f;
        public float distance=20f;

		private void Start()
		{
			// get the components on the object we need ( should not be null due to require component so no need to check )
			agent = GetComponentInChildren<UnityEngine.AI.NavMeshAgent>();
			character = GetComponent<Enemy1Character>();

			agent.updateRotation = false;
			agent.updatePosition = true;
		}


		private void Update()
		{
             if (target != null)
                distance= Vector3.Distance(target.position, transform.position);


            if(distance <= lookRadius){
                agent.SetDestination(target.position);
                character.Move (agent.desiredVelocity, false, false);    
                
                if (agent.remainingDistance < agent.stoppingDistance)
                character.Attack();
            }else
                character.Move (Vector3.zero, false, false);    
        }

		public void SetTarget(Transform target)
		{
			this.target = target;
		}
        
        void OnDrawGizmosSelected()
        {
            Gizmos.color = Color.red;
            Gizmos.DrawWireSphere(transform.position, lookRadius);
        }
}
